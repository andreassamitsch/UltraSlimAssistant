#!/usr/bin/env python3
"""Read-only recursive archive analysis. Never execute archive contents."""
import argparse
import collections
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile

GIB = 1024 ** 3
MAX_DOWNLOAD = 2 * GIB
MAX_NESTED = 4 * GIB
MAX_DECLARED = 24 * GIB
SKIP_ROOT = re.compile(r"^(?:gcc|coreutils|bash|findutils|fribidi|elfutils|cryptsetup|e2fsprogs|dibbler|DirectFB|exfat)(?:[.\-_]|$)", re.I)
SKIP_TEST_PATH = re.compile(r"(?:^|/)(?:tests?|testsuite|testdata|fuzz|benchmarks?)(?:/|$)", re.I)
MAX_TEXT = 2 * 1024 ** 2
MAX_ENTRIES = 600_000
MAX_DEPTH = 6
ARCHIVE_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2",
                    ".tar.xz", ".txz", ".tar.zst", ".tzst", ".7z", ".rar")
TEXT_SUFFIXES = (".c", ".h", ".cc", ".cpp", ".hpp", ".s", ".dts", ".dtsi", ".py",
                 ".sh", ".xml", ".json", ".ini", ".conf", ".cfg", ".service",
                 ".socket", ".rules", ".spec", ".cmake", ".mk", ".txt", ".md",
                 ".java", ".lua", ".js", ".policy", ".config", ".patch", ".bb")
PATTERNS = {
    "hyperuart": re.compile(r"hyper[-_ ]?uart|hyperUARTSetting|AT[-_ ]?HUB", re.I),
    "platform": re.compile(r"\bmt8532\b|SAT-MT8532D24WWC|\bmt853[0-9]\b", re.I),
    "debug_interfaces": re.compile(r"\bsdbd\b|smart development bridge|developerMode|serialLogSetting|usbnet|rndis|cdc_ether", re.I),
    "service_management": re.compile(r"samsung-service-manager|downloadableApp|appUpgrade|pkgmgr|tizen[-_]service|appcore|aul_launch_app", re.I),
    "audio_capture": re.compile(r"audio_in_(?:create|prepare|read|start)|snd_pcm_(?:capture|readi|open)|SNDRV_PCM_STREAM_CAPTURE|SND_PCM_STREAM_CAPTURE|audio[-_]capture", re.I),
    "microphone_dsp": re.compile(r"microphone|micbias|dmic|pdm_mic|farfield|far.field|echo.cancel|wakeword|wake.word", re.I),
    "voice_service": re.compile(r"\b(?:alexa|avsdevice|AVSCommon|AudioInputProcessor|SpeechRecognizer|wakeword|wake_word|voiceassistant|voice_assistant|voice-assistant|voiceinteraction)\b", re.I),
    "audio_frontend": re.compile(r"\b(?:mtkffp|mtkpreaec|ffp_in|plug_ffp_4_2|Capture_Mic_normal|Capture_Mic_ais_only|Capture_Echo_Reference|UL2_CM1_DMIC_8ch|UL3_2ch_GASRC_DLM)\b", re.I),
    "audio_focus": re.compile(r"\b(?:AudioFocus|FocusManager|ChannelObserver|audio_focus|audio_ducking|ducking|audio_session|sound_policy)\b", re.I),
    "mic_privacy": re.compile(r"\b(?:mic_mute|microphone_mute|microphoneMute|micmute|privacy_mute|hardware_mute|recorder_privilege)\b", re.I),
    "security_model": re.compile(r"\bsmack\b|tizen\.org/privilege/(?:recorder|microphone)|app[-_]signature|security-manager", re.I),
}
# Prefer product-specific evidence over generic third-party tests and translations.
def score(path, line, category):
    p = path.lower()
    n = 0
    if "mt853" in p or "samsung" in p or "hyperuart" in p:
        n += 7
    if "drivers/" in p or "sound/" in p or "device/" in p:
        n += 3
    if "test" in p or "/doc" in p or "locale" in p:
        n -= 3
    if category == "hyperuart":
        n += 8
    if category in ("voice_service", "audio_frontend", "audio_focus", "mic_privacy"):
        if any(part in p for part in ("mdp_alsa", "swdsp", "mas_thread", "avsdk", "pulseaudio", "tizen-manifest")):
            n += 12
        if any(part in p for part in ("drivers/gpu", "/translations/", "/examples/")):
            n -= 8
    if "define" in line or "config " in line or "compatible" in line:
        n += 2
    return n

def safe_text(s, limit=280):
    return "".join(c if c.isprintable() else " " for c in str(s)).replace("::", ": :")[:limit]

def is_archive(name):
    return name.lower().endswith(ARCHIVE_SUFFIXES)

def is_text(name):
    n = name.lower().rsplit("/", 1)[-1]
    return n.endswith(TEXT_SUFFIXES) or n in ("makefile", "kconfig", "config", "license", "copying", "readme") or n.startswith(("kconfig.", "defconfig"))

class Limit(Exception):
    pass

class Scan:
    def __init__(self, work):
        self.work = Path(work)
        self.counts = collections.Counter()
        self.suffixes = collections.Counter()
        self.matches = collections.Counter()
        self.matched_files = collections.Counter()
        self.hits = collections.defaultdict(list)
        self.archives = []
        self.root_entries = []
        self.issues = []
    def issue(self, path, reason):
        self.counts["issues"] += 1
        if len(self.issues) < 40:
            self.issues.append((safe_text(path, 500), safe_text(reason)))
    def scan_text(self, path, stream, size):
        if size > MAX_TEXT:
            self.counts["large_text_skipped"] += 1
            return
        data = stream.read(MAX_TEXT + 1)
        if len(data) > MAX_TEXT or b"\0" in data:
            self.counts["binary_or_oversize_text"] += 1
            return
        self.counts["text_files"] += 1
        self.counts["text_bytes"] += len(data)
        found = collections.Counter()
        for lineno, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
            for category, pattern in PATTERNS.items():
                m = pattern.search(line)
                if not m:
                    continue
                self.matches[category] += 1
                found[category] += 1
                if found[category] > 4:
                    continue
                excerpt = line[max(0, m.start() - 90):m.end() + 150].strip()
                item = (score(path, line, category), safe_text(path, 600), lineno, safe_text(excerpt))
                h = self.hits[category]
                h.append(item)
                if len(h) > 60:
                    h.sort(reverse=True)
                    del h[30:]
        for category in found:
            self.matched_files[category] += 1
    def member(self, path, name, size, opener, depth):
        self.counts["entries"] += 1
        if depth == 0 and SKIP_ROOT.match(name.rsplit("/", 1)[-1]):
            self.counts["generic_root_skipped"] += 1
            return
        if depth > 0 and SKIP_TEST_PATH.search(name):
            self.counts["test_entries_skipped"] += 1
            return
        self.counts["declared_bytes"] += size
        if self.counts["entries"] > MAX_ENTRIES or self.counts["declared_bytes"] > MAX_DECLARED:
            raise Limit("global entry/declared-size budget reached")
        # Member names are labels only, never filesystem destinations.
        if depth == 0 and len(self.root_entries) < 80:
            self.root_entries.append((safe_text(name, 400), size))
        self.suffixes[Path(name).suffix.lower() or "(none)"] += 1
        if is_archive(name):
            if depth >= MAX_DEPTH or size > MAX_NESTED:
                self.issue(path, "nested archive depth/size limit")
                return
            with opener() as src, tempfile.NamedTemporaryFile(dir=self.work) as tmp:
                total = 0
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > MAX_NESTED or total > size:
                        raise Limit("nested archive actual size exceeds budget")
                    tmp.write(chunk)
                tmp.flush()
                self.archive(Path(tmp.name), path, depth+1)
        elif is_text(name):
            with opener() as src:
                self.scan_text(path, src, size)
    def archive(self, file, label, depth=0):
        self.archives.append(safe_text(label, 600))
        try:
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file) as z:
                    if depth == 0:
                        print("=== Complete outer ZIP directory ===", flush=True)
                        for entry in z.infolist()[:300]:
                            if not entry.is_dir():
                                print("OUTER", safe_text(entry.filename, 500), entry.file_size, flush=True)
                    for m in z.infolist():
                        if m.is_dir():
                            continue
                        if stat.S_ISLNK(m.external_attr >> 16):
                            self.counts["links_skipped"] += 1
                            continue
                        self.member(label+"!/"+m.filename, m.filename, m.file_size,
                                    lambda m=m: z.open(m), depth)
            elif tarfile.is_tarfile(file):
                with tarfile.open(file, "r:*") as t:
                    for m in t:
                        if not m.isfile():
                            self.counts["nonregular_skipped"] += 1
                            continue
                        self.member(label+"!/"+m.name, m.name, m.size,
                                    lambda m=m: t.extractfile(m), depth)
            else:
                self.issue(label, "unsupported or invalid archive format")
        except Limit:
            raise
        except (OSError, EOFError, ValueError, RuntimeError, tarfile.TarError, zipfile.BadZipFile, NotImplementedError) as e:
            self.issue(label, type(e).__name__)
    def report(self):
        print("=== Archive inventory ===")
        for a in self.archives[:100]:
            print("  ARCHIVE", a)
        for n, s in self.root_entries:
            print("  MEMBER", n, s)
        print("Counts:", dict(self.counts))
        print("Top suffixes:", self.suffixes.most_common(25))
        print("=== Source evidence (selected matches, not a complete source listing) ===")
        for category in PATTERNS:
            print(category, "lines", self.matches[category], "files", self.matched_files[category])
            for _, p, line, excerpt in sorted(self.hits[category], reverse=True)[:22]:
                print(f"  {p}:{line}: {excerpt}")
        for p, why in self.issues:
            print("  LIMIT/ERROR", p, why)
        print("Coverage is incomplete if issues, skipped large text, unsupported archive formats or global limits are reported.")

def pcloud_download(work):
    raw = os.environ.get("PCLOUD_SOURCE_LINK", "").strip()
    if not raw:
        raise ValueError("repository secret PCLOUD_SOURCE_LINK is missing")
    if raw.startswith("https://"):
        u = urllib.parse.urlsplit(raw)
        if u.hostname != "e.pcloud.link" or u.path != "/publink/show":
            raise ValueError("expected European pCloud share URL")
        code = urllib.parse.parse_qs(u.query).get("code", [""])[0]
    else:
        code = raw
    if not re.fullmatch(r"[a-zA-Z0-9]{10,100}", code):
        raise ValueError("invalid pCloud share code format")
    # Never print the code, API URL, resolved download URL, response body, or raw exception.
    class HTTPSOnly(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            u = urllib.parse.urlsplit(newurl)
            if u.scheme != "https" or not trusted(u.hostname or ""):
                raise ValueError("unexpected redirect host")
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    def trusted(host):
        return host == "pcloud.com" or host.endswith(".pcloud.com") or host == "pcloudusercontent.com" or host.endswith(".pcloudusercontent.com")
    op = urllib.request.build_opener(HTTPSOnly())
    def api(method):
        url = "https://eapi.pcloud.com/" + method + "?" + urllib.parse.urlencode({"code": code})
        with op.open(url, timeout=30) as resp:
            body = json.loads(resp.read(1024*1024))
        result = body.get("result")
        if result != 0:
            raise ValueError(f"pCloud {method} error code {result}")
        return body
    metadata = api("showpublink").get("metadata", {})
    name = metadata.get("name", "")
    if metadata.get("isfolder") or not re.fullmatch(r"HW-(?:Q(?:800|990)D|S800D)(?:[_-]EN)?\.zip", name, re.I):
        raise ValueError("shared item is not an expected Samsung source archive")
    size = int(metadata.get("size", 0))
    if not 0 < size <= MAX_DOWNLOAD:
        raise ValueError("archive size missing or exceeds download budget")
    print("Share metadata verified:", name, size, "bytes", flush=True)
    link = api("getpublinkdownload")
    host = next((h for h in link.get("hosts", []) if trusted(h)), None)
    path = link.get("path", "")
    if not host or not path.startswith("/") or path.startswith("//"):
        raise ValueError("unexpected download host or path")
    dest = Path(work) / "source.zip"
    digest = hashlib.sha256()
    count = 0
    with op.open("https://" + host + path, timeout=60) as resp, dest.open("wb") as out:
        while True:
            chunk = resp.read(1024*1024)
            if not chunk:
                break
            count += len(chunk)
            if count > size or count > MAX_DOWNLOAD:
                raise ValueError("download exceeds expected size")
            out.write(chunk)
            digest.update(chunk)
    if count != size or not zipfile.is_zipfile(dest):
        raise ValueError("download length or ZIP validation failed")
    print("Downloaded:", name, count, "bytes, SHA256", digest.hexdigest(), flush=True)
    return dest, name

def self_test():
    with tempfile.TemporaryDirectory() as work:
        nested = io.BytesIO()
        with tarfile.open(fileobj=nested, mode="w:gz") as t:
            for name, data in [("drivers/mt8532/hyperuart.c", b"int hyperuart_init(void);\n"), ("sound/audio.c", b"snd_pcm_open();\n")]:
                ti = tarfile.TarInfo(name)
                ti.size = len(data)
                t.addfile(ti, io.BytesIO(data))
        archive = Path(work) / "test.zip"
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("source.tar.gz", nested.getvalue())
            z.writestr("../outside.c", "audio_in_create();\n")
            z.writestr("mdp_alsa/swdsp/aasound.conf",
                       "pcm.ffp_in { type mtkffp }\nmic_mute=1\n")
            z.writestr("avsdk/voice.cpp",
                       "AudioInputProcessor; FocusManager;\n")
        s = Scan(work)
        s.archive(archive, "test.zip")
        assert s.matched_files["hyperuart"] == 1
        assert s.matched_files["audio_capture"] == 2
        for category in ("voice_service", "audio_frontend", "audio_focus", "mic_privacy"):
            assert s.matched_files[category] == 1, category
        assert len(s.archives) == 2
        assert not (Path(work).parent / "outside.c").exists()
        assert not s.issues
        print("PASS: nested ZIP/TAR.GZ, source matching, path traversal names not extracted")
        s.report()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--work")
    p.add_argument("--archive", type=Path,
                   help="Analyze a locally supplied public source ZIP instead of pCloud")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.work:
        p.error("--work required")
    try:
        if args.archive is not None:
            archive = args.archive.resolve()
            name = archive.name
            if not archive.is_file() or not 0 < archive.stat().st_size <= MAX_DOWNLOAD or not zipfile.is_zipfile(archive):
                raise ValueError("invalid or oversize local source ZIP")
            digest = hashlib.sha256()
            with archive.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            print("Local archive:", safe_text(name), archive.stat().st_size, "bytes, SHA256", digest.hexdigest())
        else:
            archive, name = pcloud_download(args.work)
    except ValueError as e:
        # Only locally created errors are safe to log; parsing errors may embed URLs.
        print("Download validation failed:", type(e).__name__)
        if str(e).startswith(("repository secret", "expected European", "invalid pCloud", "pCloud showpublink error code", "pCloud getpublinkdownload error code", "shared item", "archive size", "unexpected download", "download exceeds", "download length", "invalid or oversize local source ZIP")):
            print(safe_text(e))
        raise SystemExit(2)
    except Exception as e:
        print("Download failed:", type(e).__name__, getattr(e, "code", ""))
        raise SystemExit(2)
    s = Scan(args.work)
    try:
        s.archive(archive, name)
    except Limit as e:
        s.issue(name, str(e))
    s.report()
    if s.counts["issues"]:
        print("WARNING: incomplete archive coverage")
    print("Selected scan intentionally omits generic compiler/tool and test trees.")
if __name__ == "__main__":
    main()
