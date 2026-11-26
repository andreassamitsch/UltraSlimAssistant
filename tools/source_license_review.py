#!/usr/bin/env python3
"""Read license metadata from selected released media/SDK source files; no extraction."""
import collections
import hashlib
import io
import re
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path
from source_analysis import pcloud_download, safe_text

ROOTS={"tzav-media-mt8532.zip","avsdk-lib-releaser.zip","system_drv.tgz","tzav-micom.tgz"}
ARCHIVES=(".zip",".tgz",".tar",".tar.gz",".tar.xz",".tar.bz2")
SUFFIXES={".c",".h",".cc",".cpp",".hpp",".conf",".cfg",".xml",".mk",".spec",".sh",".txt",".md"}
SPDX=re.compile(r"SPDX-License-Identifier:\s*([A-Za-z0-9.+\-() :]+)",re.I)
MARKERS={
    "GPL":re.compile(r"GNU (?:General|Library) Public License|GPL version [23]",re.I),
    "LGPL":re.compile(r"GNU Lesser General Public License|LGPL",re.I),
    "Apache":re.compile(r"Apache License|Apache-2\.0",re.I),
    "MIT/BSD":re.compile(r"permission is hereby granted|redistribution and use in source and binary forms",re.I),
    "restricted":re.compile(r"confidential|proprietary|not be disclosed|no reproduction|unauthorized copying",re.I)
}
LIMIT=256*1024**2
def walk(file,label,depth=0):
    if depth>5: return
    if zipfile.is_zipfile(file):
        with zipfile.ZipFile(file) as z:
            for m in z.infolist():
                if not m.is_dir():
                    yield from member(m.filename,m.file_size,lambda m=m:z.open(m),label,depth)
    else:
        file.seek(0)
        with tarfile.open(fileobj=file,mode="r:*") as t:
            for m in t:
                if m.isfile():
                    yield from member(m.name,m.size,lambda m=m:t.extractfile(m),label,depth)
def member(name,size,reader,parent,depth):
    if size<0 or size>LIMIT or re.search(r"password|credential|private[-_]?key|\.(?:pem|p12|pfx|key)$",name,re.I): return
    path=parent+"!/"+name
    if name.lower().endswith(ARCHIVES):
        with reader() as f: data=f.read(size+1)
        if len(data)!=size: return
        yield from walk(io.BytesIO(data),path,depth+1)
    elif Path(name).suffix.lower() in SUFFIXES or re.search(r"(?:^|/)(?:COPYING|LICENSE|Makefile|Kconfig)$",name,re.I):
        with reader() as f: data=f.read(min(size,16384))
        if b"\0" in data: return
        h=data.decode("utf-8","replace")
        # Inspect header only; record labels, not vendor source excerpts.
        spdx=SPDX.search(h)
        tags=[k for k,p in MARKERS.items() if p.search(h)]
        if spdx: tags.append("SPDX:"+safe_text(spdx.group(1).strip(),100))
        if re.search(r"(?:^|/)(?:COPYING|LICENSE|OpenSourceAnnouncement)[^/]*$",name,re.I): tags.append("notice-file")
        yield path,tags

def main():
    with tempfile.TemporaryDirectory() as work:
        archive,model=pcloud_download(work)
        if model!="HW-Q800D.zip": raise SystemExit("unexpected reference model")
        with zipfile.ZipFile(archive) as outer:
            for m in outer.infolist():
                if Path(m.filename).name not in ROOTS: continue
                if m.file_size>LIMIT: raise SystemExit("root size limit")
                raw=outer.read(m)
                counts=collections.Counter()
                selected=[]
                for path,tags in walk(io.BytesIO(raw),Path(m.filename).name):
                    counts["files"]+=1
                    if not tags: counts["unclassified"]+=1
                    for tag in tags: counts[tag]+=1
                    relevant=re.search(r"mdp_alsa|aasound|asound|smartthings.av|tizen-manifest|install_driver|system_drv|micom|ffp",path,re.I)
                    if tags or relevant:
                        selected.append((bool(relevant),bool(tags),path,tags))
                print("LICENSE_SCREEN",Path(m.filename).name,dict(counts))
                for _,_,path,tags in sorted(selected,reverse=True)[:100]:
                    print("HEADER",safe_text(path,550),"|",", ".join(tags) or "unclassified")
        print("Header labels are preliminary evidence, not a component-wide redistribution grant.")
if __name__=="__main__": main()
