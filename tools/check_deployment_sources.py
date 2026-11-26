#!/usr/bin/env python3
"""Read-only inventory of published build flags and deployment component presence.
Print metadata only; never execute vendor code or inspect signing material."""
import hashlib
import pathlib
import re
import tarfile
import tempfile
import zipfile
from source_analysis import pcloud_download

EXPECTED="bd55f6bf95713a93df1feab53a7f4c9cd93dcc3b5d2526cb35dbdc4d8c91b650"
FLAG=re.compile(r"\b(?:CONFIG_)?SAMSUNG_(?:USBNET_HYPERUART_IFNAME|HYPERUART_PREALLOC_SUPPORT|HYPERUART_SDB_PUSH_FIX)\b")
DEPLOY=re.compile(r"(?:^|[/_.-])(?:sdbd|sdb|pkgmgr|tpk-backend|app-manager|appmanager|service-manager|hyperuart)(?:$|[/_.-])",re.I)
def main():
    with tempfile.TemporaryDirectory() as work:
        path,model=pcloud_download(work)
        with open(path,"rb") as f:
            if model!="HW-Q800D.zip" or hashlib.file_digest(f,"sha256").hexdigest()!=EXPECTED:
                raise RuntimeError("archive identity mismatch")
        with zipfile.ZipFile(path) as z:
            names=[m.filename for m in z.infolist() if not m.is_dir()]
            print("OUTER_FILES",len(names),"DEPLOYMENT_NAMED_COMPONENTS",sum(bool(DEPLOY.search(n)) for n in names),flush=True)
            kernel=next(m for m in z.infolist() if pathlib.PurePosixPath(m.filename).name=="linux_kernel.tgz")
            count=total=build_count=defs=refs=0
            with z.open(kernel) as f, tarfile.open(fileobj=f,mode="r|*") as t:
                for m in t:
                    if not m.isfile(): continue
                    count+=1;total+=m.size
                    if count>350000 or total>12*1024**3: raise RuntimeError("inspection limit")
                    name=m.name
                    basename=pathlib.PurePosixPath(name).name
                    if DEPLOY.search(name):
                        print("KERNEL_DEPLOYMENT_NAMED_FILE",name[:300],flush=True)
                    if m.size>2*1024**2: continue
                    if not (basename.endswith((".h",".c",".mk",".config","defconfig")) or basename.startswith(("Makefile","Kconfig"))): continue
                    raw=t.extractfile(m).read()
                    if b"SAMSUNG_" not in raw and not basename.endswith("defconfig"): continue
                    for i,line in enumerate(raw.decode("utf-8","replace").splitlines(),1):
                        flags=FLAG.findall(line)
                        if not flags: continue
                        if re.search(r"^\s*#\s*define\s+|^\s*config\s+|^\s*CONFIG_.*=|(?:-D)SAMSUNG_",line):
                            defs+=1;kind="definition-or-build-setting"
                        else:
                            refs+=1;kind="reference"
                        if defs+refs<=180:
                            print("FLAG",kind,name[:250],i,",".join(flags),flush=True)
                    if basename=="MT8532_release_defconfig":
                        build_count+=1
                        for flag in ("CONFIG_SAMSUNG_USBNET_HYPERUART_IFNAME","CONFIG_SAMSUNG_HYPERUART_SDB_PUSH_FIX","CONFIG_SAMSUNG_HYPERUART_PREALLOC_SUPPORT"):
                            data=raw.decode("utf-8","replace")
                            match=re.search(r"^"+flag+r"=([ymn])$",data,re.M)
                            absent=re.search(r"^# "+flag+r" is not set$",data,re.M)
                            print("MT8532_CONFIG",flag,match.group(1) if match else "not-set" if absent else "not-listed",flush=True)
            print("KERNEL_SUMMARY",count,"files",build_count,"target_configs",defs,"definitions_or_build_settings",refs,"references",flush=True)
            for m in z.infolist():
                if pathlib.PurePosixPath(m.filename).name not in {"avsdk-lib-releaser.zip","tzav-media-mt8532.zip","system_drv.tgz","tzav-micom.tgz"}: continue
                with tempfile.NamedTemporaryFile(dir=work) as dst:
                    with z.open(m) as f:
                        while chunk:=f.read(1024**2): dst.write(chunk)
                    dst.flush()
                    if zipfile.is_zipfile(dst.name):
                        with zipfile.ZipFile(dst.name) as a: names=a.namelist()
                    else:
                        with tarfile.open(dst.name) as a: names=a.getnames()
                    matches=[n for n in names if DEPLOY.search(n)]
                    print("SELECTED_COMPONENT",pathlib.PurePosixPath(m.filename).name,"entries",len(names),"deployment_name_matches",len(matches),flush=True)
    print("NOTE: filename and build flag evidence only; not a firmware runtime or signature-policy audit.",flush=True)
if __name__=="__main__":main()
