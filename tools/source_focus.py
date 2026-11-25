#!/usr/bin/env python3
"""Read specific released source components without executing or extracting them."""
import collections
import io
import re
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from source_analysis import pcloud_download, safe_text

TARGETS = {
    "avsdk-lib-releaser.zip",
    "tzav-media-mt8532.zip",
    "pulseaudio.zip",
    "tzav-micom.tgz",
    "system_drv.tgz",
}
RELEVANT = re.compile(r"audio_in_|(?:snd_pcm|pcm)_(?:open|read|capture)|(?:audio|mic|microphone|voice|pcm|record|stream)[_\w-]{0,40}(?:capture|record|input|read|source|stream)|(?:capture|record|input|source)[_\w-]{0,40}(?:audio|mic|pcm)|pa_source_(?:new|put|post)|pa_stream_connect_record|echo[-_ ]?cancel|far[-_ ]?field|wake[-_ ]?word|service_application|service-app|pkgmgr|tpk-backend", re.I)
NAME = re.compile(r"(?:audio|mic|capture|record|source|stream|alsa|pulse|aec|voice|manifest|readme|config|cmake|makefile|kconfig)", re.I)
TEXT = re.compile(r"\.(?:c|h|cc|cpp|hpp|xml|md|txt|conf|cfg|spec|sh|in|am|mk|service|dts|dtsi)$|(?:^|/)(?:makefile|readme|kconfig)(?:$|\.)", re.I)
PRIVATE = re.compile(r"(?:\.(?:p12|pfx|pem|key|crt)$|password|credential|private[-_]?key|signer)", re.I)

def out(msg):
    print(safe_text(msg, 900), flush=True)

def inspect(label, entries):
    counts=collections.Counter()
    paths=[]
    selected=[]
    for name,size,reader in entries:
        counts["members"]+=1
        if PRIVATE.search(name):
            continue
        if NAME.search(name):
            paths.append((name,size))
        if not TEXT.search(name) or size>1024*1024:
            continue
        if re.search(r"(?:^|/)(?:tests?|docs?|po|locale|examples?)(?:/|$)",name,re.I) and not re.search(r"smartthings_av_doc|readme",name,re.I):
            continue
        try:
            raw=reader()
        except Exception:
            counts["read_errors"]+=1
            continue
        if b"\x00" in raw:
            continue
        counts["text_files"]+=1
        lines=raw.decode("utf-8","replace").splitlines()
        hits=[i for i,line in enumerate(lines) if RELEVANT.search(line)]
        if not hits and not re.search(r"(?:tizen-manifest\.xml|/README\.md|/main\.cpp)$",name,re.I):
            continue
        counts["matching_files"]+=1
        score=0
        if re.search(r"mt8532|smartthings_av_stream|smartthings_av_content_upload|tizen-manifest|main\.cpp",name,re.I):score+=20
        if re.search(r"audio|alsa|voice|capture|record|source",name,re.I):score+=5
        if re.search(r"test|third.party|/doc",name,re.I):score-=8
        selected.append((score,name,hits,lines))
        if len(selected)>100:
            selected.sort(key=lambda x:(x[0],x[1]),reverse=True)
            selected=selected[:55]
    out(f"=== {label} {dict(counts)} ===")
    for name,size in paths[:150]: out(f"PATH {name} {size}")
    for score,name,hits,lines in sorted(selected,key=lambda x:(x[0],x[1]),reverse=True)[:22]:
        out(f"FILE {name} ({len(lines)} lines, {len(hits)} matching lines)")
        # For short manifests and main source, read actual whole public source.
        if len(lines)<=110 and re.search(r"tizen-manifest\.xml|/README\.md|/main\.cpp",name,re.I):
            ids=range(len(lines))
        else:
            ids=sorted({j for i in hits[:12] for j in range(max(0,i-2),min(len(lines),i+3))})
        for i in ids:
            if not PRIVATE.search(lines[i]): out(f"{i+1}: {lines[i]}")

def main(work):
    try:
        archive,name=pcloud_download(work)
    except Exception as e:
        out(f"Download failed: {type(e).__name__}")
        raise SystemExit(2)
    with zipfile.ZipFile(archive) as outer:
        for m in outer.infolist():
            if Path(m.filename).name not in TARGETS: continue
            if m.file_size>256*1024**2: raise SystemExit("component exceeds limit")
            raw=outer.read(m)
            stream=io.BytesIO(raw)
            if zipfile.is_zipfile(stream):
                with zipfile.ZipFile(stream) as z:
                    inspect(m.filename, ((x.filename,x.file_size,lambda x=x:z.read(x)) for x in z.infolist() if not x.is_dir()))
            else:
                stream.seek(0)
                with tarfile.open(fileobj=stream,mode="r:*") as t:
                    inspect(m.filename, ((x.name,x.size,lambda x=x:t.extractfile(x).read()) for x in t if x.isfile()))
if __name__=="__main__":
    main(sys.argv[1])
