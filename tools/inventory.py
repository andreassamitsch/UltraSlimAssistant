#!/usr/bin/env python3
"""Read-only inventory of a vendor ZIP; no extraction or binary execution."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

def inventory(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        return {
            "archive": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": digest.hexdigest(),
            "member_count": len(members),
            "uncompressed_bytes": sum(m.file_size for m in members),
            "members_truncated": len(members) > 200,
            "members": [
                {"name": m.filename, "size_bytes": m.file_size,
                 "compressed_bytes": m.compress_size,
                 "encrypted_zip_member": bool(m.flag_bits & 1)}
                for m in members[:200]
            ],
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(inventory(args.archive), indent=2, ensure_ascii=True))
