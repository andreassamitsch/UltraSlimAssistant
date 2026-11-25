#!/usr/bin/env python3
"""Focused inventory of published Linux and audio build artifacts, not installation."""
import collections
import io
import re
import sys
import tarfile
import zipfile
from pathlib import Path
from source_analysis import pcloud_download, safe_text

def out(s):
    print(safe_text(s, 600), flush=True)

AUDIO = re.compile(r"\b(?:CONFIG_[A-Z0-9_]*(?:SND|ALSA|AUDIO|DMIC|PDM|MT853)[A-Z0-9_]*|KCTRL_[A-Z0-9_]*(?:MIC|CAPTURE|RECORD|VOICE)[A-Z0-9_]*|SNDRV_PCM_STREAM_CAPTURE|SND_PCM_STREAM_CAPTURE|snd_pcm_(?:open|readi)|pa_stream_connect_record|pa_source_new)\b|(?:microphone|far.field|echo.cancel|wake.word|pcm.capture)",re.I)
PLATFORM = re.compile(r"(?:mt853[0-9]|tzav|mediatek|hyperuart|vdfs|samsung)",re.I)
PRIVATE = re.compile(r"(?:\.(?:p12|pfx|pem|key|crt)$|password|credential|private[-_]?key|signer)",re.I)
SOURCE = re.compile(r"\.(?:c|h|cc|cpp|hpp|dts|dtsi|conf|cfg|xml|md|txt|mak|spec|service|in|am)$|(?:^|/)(?:makefile|kconfig|readme|[^/]*defconfig)(?:$|\.)",re.I)
def emit_lines(name,data,pat,limit=35):
    if b"\x00" in data: return
    lines=data.decode("utf-8","replace").splitlines()
    hits=[(i,l) for i,l in enumerate(lines,1) if pat.search(l) and not PRIVATE.search(l)]
    if not hits:return
    out(f"FILE {name}: {len(lines)} lines, {len(hits)} matching")
    for i,l in hits[:limit]:out(f"{i}: {l}")
def inspect_kernel(raw):
    count=0; total=0; paths=[]; configs=[]; roots=collections.Counter(); sources=[]
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r|*") as t:
        for x in t:
            if not x.isfile():continue
            count+=1;total+=x.size
            if count>350000 or total>12*1024**3:
                out("LIMIT kernel scan");break
            n=x.name
            roots["/".join(n.split("/")[:2])]+=1
            if PRIVATE.search(n):continue
            if re.search(r"(?:^|/)(?:[^/]*defconfig|\.config)$",n,re.I) and re.search(r"mt853|tzav|samsung|av|tv|mediatek",n,re.I):
                configs.append(n)
                if x.size<512*1024:emit_lines(n,t.extractfile(x).read(),AUDIO,55)
            elif re.search(r"(?:^|/)Makefile$",n) and len(n.strip("./").split("/"))<=2 and x.size<100000:
                data=t.extractfile(x).read()
                emit_lines(n,data,re.compile(r"^(?:VERSION|PATCHLEVEL|SUBLEVEL|EXTRAVERSION)\s*="),8)
            elif re.search(r"hyper[-_]?uart",n,re.I):
                paths.append(n)
            elif PLATFORM.search(n) and re.search(r"(?:^|/)(?:sound|audio|asoc|dts|pcm|mic|alsa)(?:/|[._-])|mt853[0-9]",n,re.I):
                paths.append(n)
                if SOURCE.search(n) and x.size<512*1024 and len(sources)<100:
                    data=t.extractfile(x).read()
                    if AUDIO.search(data.decode("utf-8","replace")):
                        sources.append(n)
                        emit_lines(n,data,AUDIO,12)
    out(f"KERNEL entries={count} declared_bytes={total} config_paths={len(configs)} selected_source_paths={len(paths)}")
    out(str(roots.most_common(25)))
    for n in configs[:80]:out("CONFIG "+n)
    for n in paths[:180]:out("KERNEL_PATH "+n)

def inspect_media(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for m in z.infolist():
            if m.is_dir() or PRIVATE.search(m.filename):continue
            out(f"MEDIA {m.filename} {m.file_size}")
            if m.filename.endswith("mdp_alsa.tgz") and m.file_size<100*1024**2:
                with tarfile.open(fileobj=io.BytesIO(z.read(m)),mode="r|*") as t:
                    count=0;total=0
                    for x in t:
                        if not x.isfile() or PRIVATE.search(x.name):continue
                        count+=1;total+=x.size
                        if count>30000 or total>2*1024**3:
                            out("LIMIT MDP archive");break
                        if count<=180:out(f"MDP_PATH {x.name} {x.size}")
                        if SOURCE.search(x.name) and x.size<512*1024:
                            emit_lines(x.name,t.extractfile(x).read(),AUDIO,15)
                    out(f"MDP entries={count} declared_bytes={total}")
            elif SOURCE.search(m.filename) and m.file_size<1024*1024:
                emit_lines(m.filename,z.read(m),AUDIO,35)
def inspect_pulse(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for x in z.infolist():
            n=x.filename
            if x.is_dir() or PRIVATE.search(n):continue
            if re.search(r"pulseaudio-tv\.service|/system\.pa\.in$|/default\.pa\.in$|/packaging/pulseaudio\.spec$|/meson_options\.txt$",n):
                out("PULSE_CONFIG "+n)
                emit_lines(n,z.read(x),re.compile(r"ExecStart|Description|(?:load-module|enable|disable|with|without).*(?:alsa|source|echo|audio|tizen)|^Version:|system-mode|module-udev-detect",re.I),45)
            elif re.search(r"(?:tizen|samsung|tv|hal|alsa|echo-cancel)",n,re.I) and re.search(r"/modules/",n):
                out("PULSE_MODULE "+n)
def main(work):
    try:
        archive,name=pcloud_download(work)
    except Exception as e:
        out(f"Download failed: {type(e).__name__}");raise SystemExit(2)
    with zipfile.ZipFile(archive) as z:
        for m in z.infolist():
            n=Path(m.filename).name
            if n not in {"linux_kernel.tgz","tzav-media-mt8532.zip","pulseaudio.zip"}:continue
            if m.file_size>300*1024**2:raise SystemExit("component size limit")
            out("=== "+n+" ===")
            raw=z.read(m)
            {"linux_kernel.tgz":inspect_kernel,"tzav-media-mt8532.zip":inspect_media,"pulseaudio.zip":inspect_pulse}[n](raw)
if __name__=="__main__":
    main(sys.argv[1])
