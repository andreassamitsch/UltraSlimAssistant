#!/usr/bin/env python3
"""Read the released MT8532 audio route definitions and trace their driver labels."""
import io
import re
import sys
import tarfile
import zipfile
from pathlib import Path
from source_analysis import pcloud_download, safe_text

def out(s):print(safe_text(s,700),flush=True)
KEY=re.compile(r"Capture_Mic|Capture_Voice|Capture_Echo|VOICE_UPLOAD|ECHO_REF|MIC_NORMAL|MIC_AIS|(?:voice|mic|echo)[_\- ]*(?:upload|capture|reference|normal|ais)|(?:capture|upload)[_\- ]*(?:mic|voice)|\b(?:MIC_IN|DMIC|AMIC)\b",re.I)
LABEL=re.compile(r"\.(?:name|stream_name|cpu_dai_name|codec_dai_name|dpcm_capture|capture|channels_min|channels_max|rates|formats)\s*=|SND_SOC_DAPM.*(?:MIC|ADC)",re.I)
def main(work):
    try:
        archive,name=pcloud_download(work)
    except Exception as e:
        out(f"Download failed: {type(e).__name__}");raise SystemExit(2)
    with zipfile.ZipFile(archive) as outer:
        m=next(x for x in outer.infolist() if Path(x.filename).name=="tzav-media-mt8532.zip")
        if m.file_size>50*1024**2:raise SystemExit("Media archive limit")
        with zipfile.ZipFile(io.BytesIO(outer.read(m))) as z:
            p=next(x for x in z.infolist() if x.filename.endswith("mdp_alsa.tgz"))
            if p.file_size>50*1024**2:raise SystemExit("ALSA archive limit")
            with tarfile.open(fileobj=io.BytesIO(z.read(p)),mode="r|*") as t:
                count=0;total=0
                for f in t:
                    if not f.isfile():continue
                    count+=1;total+=f.size
                    if count>10000 or total>1024**3:raise SystemExit("ALSA member limit")
                    n=f.name
                    if f.size>1024**2 or not re.search(r"\.(?:c|h|conf|dts|dtsi|xml|mk|txt|md)$|/Makefile$",n,re.I):continue
                    d=t.extractfile(f).read()
                    if b"\x00" in d:continue
                    lines=d.decode("utf-8","replace").splitlines()
                    if n.endswith(("/asound.conf","/aasound.conf")):
                        out("=== FULL CONFIG "+n+" ===")
                        for i,line in enumerate(lines,1):out(f"{i}: {line}")
                        continue
                    hits=[i for i,line in enumerate(lines) if KEY.search(line)]
                    if not hits:continue
                    out(f"=== ROUTE FILE {n} lines={len(lines)} matches={len(hits)} ===")
                    ids=sorted({j for i in hits[:28] for j in range(max(0,i-3),min(len(lines),i+4))})
                    for i in ids:out(f"{i+1}: {lines[i]}")
                    if re.search(r"mt8532-(?:sound|afe-pcm)",n):
                        for i,line in enumerate(lines):
                            if LABEL.search(line) and any(abs(i-j)<=12 for j in hits):
                                out(f"DAI {i+1}: {line}")
                out(f"ALSA inventory: {count} regular entries, {total} declared bytes")
if __name__=="__main__":main(sys.argv[1])
