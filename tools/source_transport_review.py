#!/usr/bin/env python3
"""Read-only review of released transport implementation and shared package hashes."""
import hashlib
import io
import os
import re
import sys
import tarfile
import zipfile
from pathlib import Path
from source_analysis import pcloud_download, safe_text

def out(s):print(safe_text(s,600),flush=True)
SHARED={"linux_kernel.tgz","avsdk-lib-releaser.zip","pulseaudio.zip","MM_DTV.zip"}
def analyze(path,name,inspect=False):
    hashes={}
    with zipfile.ZipFile(path) as z:
        for x in z.infolist():
            n=Path(x.filename).name
            if n not in SHARED or x.is_dir():continue
            if x.file_size>300*1024**2:raise SystemExit("component size limit")
            h=hashlib.sha256()
            with z.open(x) as f:
                while True:
                    b=f.read(1024**2)
                    if not b:break
                    h.update(b)
            hashes[n]=h.hexdigest()
            out(f"COMPONENT {name} {n} sha256={hashes[n]}")
            if n!="linux_kernel.tgz" or not inspect:continue
            with z.open(x) as f, tarfile.open(fileobj=f,mode="r|*") as t:
                entries=0;total=0
                for m in t:
                    if not m.isfile():continue
                    entries+=1;total+=m.size
                    if entries>350000 or total>12*1024**3:raise SystemExit("kernel limit")
                    if m.name.endswith("/drivers/net/usb/usbnet.c") and m.size<1024**2:
                        a=t.extractfile(m).read().decode("utf-8","replace").splitlines()
                        out(f"TRANSPORT {m.name} lines={len(a)}")
                        hits=[i for i,l in enumerate(a) if re.search(r"HUART|HyperUART|hyperuart|sdbd",l,re.I)]
                        # Record references, enclosing functions and state changes without
                        # printing addresses, executable command strings or authentication data.
                        for i in hits:
                            v=a[i]
                            if re.search(r'["\x27]|(?:pass|auth|token|key)',v,re.I):
                                out(f"{i+1}: [literal/credential-related line omitted] identifiers: "+", ".join(re.findall(r"\b(?:HUART\w*|hyperuart\w*|sdbd\w*)\b",v,re.I)))
                            else:out(f"{i+1}: {v.strip()}")
                        for i,l in enumerate(a,1):
                            if re.search(r"\b(?:call_usermodehelper|kernel_execve|kthread_run|kernel_read|filp_open)\s*\(",l):
                                out(f"TRANSPORT_CALL {i}: "+re.findall(r"\b(?:call_usermodehelper|kernel_execve|kthread_run|kernel_read|filp_open)\b",l)[0])
                    elif m.name.endswith("/arch/arm/configs/MT8532_release_defconfig") and m.size<512*1024:
                        a=t.extractfile(m).read().decode("utf-8","replace").splitlines()
                        for i,l in enumerate(a,1):
                            if re.search(r"CONFIG_(?:USB_USBNET|USB_NET_CDCETHER|USB_NET_RNDIS_HOST|USB_NET_AX8817X|USB_NET_AX88179_178A|SND_PCM|SND_SOC|MACH_MT8532)(?:=| is not set)",l):
                                out(f"BUILD_CONFIG {i}: {l}")
    return hashes

def main(work):
    first=os.environ["PCLOUD_SOURCE_LINK"]
    second=os.environ["PCLOUD_Q990D_SOURCE_LINK"]
    allhash=[]
    for i,link in enumerate((first,second)):
        os.environ["PCLOUD_SOURCE_LINK"]=link
        folder=Path(work)/str(i);folder.mkdir()
        try:
            path,name=pcloud_download(folder)
        except Exception as e:
            out(f"Download failed: {type(e).__name__}");raise SystemExit(2)
        allhash.append(analyze(path,name,inspect=i==0))
        path.unlink()
    for n in sorted(SHARED):
        out(f"COMPARE {n} {'identical' if n in allhash[0] and allhash[0].get(n)==allhash[1].get(n) else 'different or missing'}")
if __name__=="__main__":main(sys.argv[1])
