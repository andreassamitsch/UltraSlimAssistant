#!/usr/bin/env python3
"""Inspect official Tizen 8.0 rootstrap, syntax-check source using actual headers.
No SDK or target binaries are executed. Not an installable package or device test."""
import hashlib
import pathlib
import subprocess
import sys
import tarfile
import tempfile
import zipfile

archive=pathlib.Path(sys.argv[1])
project=pathlib.Path(sys.argv[2]).resolve()
with archive.open("rb") as f:
    print("ROOTSTRAP_SHA256",hashlib.file_digest(f,"sha256").hexdigest(),flush=True)
with tempfile.TemporaryDirectory() as work:
    base=pathlib.Path(work)
    with zipfile.ZipFile(archive) as z:
        members=z.infolist()
        if sum(m.file_size for m in members)>2_000_000_000: raise RuntimeError("expanded ZIP budget")
        for m in members:
            p=pathlib.PurePosixPath(m.filename)
            if p.is_absolute() or ".." in p.parts or "\\" in m.filename: raise RuntimeError("unsafe SDK path")
        z.extractall(base)
    print("ZIP_ENTRIES",len(members),"SDK_ARCHIVES",flush=True)
    for p in list(base.rglob("*")):
        if p.is_file() and p.name.endswith((".tar.gz",".tar.xz",".tgz",".tar",".tar.bz2")):
            print("INNER_ARCHIVE",p.name,flush=True)
            out=p.parent/(p.name+".unpacked");out.mkdir()
            with tarfile.open(p) as t:
                entries=t.getmembers()
                if sum(m.size for m in entries)>2_000_000_000: raise RuntimeError("expanded TAR budget")
                # Extract regular files and directories only; no links/devices.
                t.extractall(out,members=[m for m in entries if m.isfile() or m.isdir()],filter="data")
    for name in ("service_app.h","sound_manager.h","system_info.h","dlog.h"):
        paths=list(base.rglob(name))
        print("HEADER",name,[str(p.relative_to(base)) for p in paths][:8],flush=True)
        if not paths: raise RuntimeError("required header missing: "+name)
    h=next(base.rglob("service_app.h"))
    roots=[p for p in h.parents if p.name=="include"]
    if not roots: raise RuntimeError("SDK include root not identified")
    inc=roots[0]
    sysroot=inc.parent.parent
    print("INCLUDE_ROOT",inc.relative_to(base),"SYSROOT",sysroot.relative_to(base),flush=True)
    # Official headers may reside in API-specific subdirectories; use all
    # directories containing headers, with root include ahead of them.
    dirs=sorted({p.parent for p in inc.rglob("*.h")})
    args=["clang","-std=gnu11","-fsyntax-only","-Werror=implicit-function-declaration","--sysroot="+str(sysroot),"-isystem",str(inc)]
    for p in dirs:
        if p!=inc: args.extend(["-isystem",str(p)])
    for name in ("service_smoke.c","capability_probe.c"):
        print("CHECK",name,flush=True)
        subprocess.run(args+[str(project/"prototype/tizen"/name)],check=True)
        print("PASS_REAL_SDK_HEADER_CHECK",name,flush=True)
