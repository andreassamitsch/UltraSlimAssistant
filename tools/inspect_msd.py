#!/usr/bin/env python3
"""Read-only, bounded inspection of the public MediaTek update container.

Never extracts, executes, decrypts or prints proprietary binary contents.
Only selected metadata tokens, checksums and aggregate statistics are emitted.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile
import zipfile

ROOT = "SAT-MT8532D24WWC/image/"
CHUNK = 1024 * 1024
MAX_IMAGE = 1024 * 1024 * 1024
MAGICS = {
    "ELF": b"\x7fELF", "gzip": b"\x1f\x8b", "ZIP": b"PK\x03\x04",
    "XZ": b"\xfd7zXZ\x00", "SquashFS": b"hsqs",
    "UBI": b"UBI#", "FIT/FDT": b"\xd0\x0d\xfe\xed",
    "Android sparse": b"\x3a\xff\x26\xed",
}
TOKENS = ("Linux", "Tizen", "ALSA", "PulseAudio", "PipeWire", "Alexa",
          "AVS", "MediaTek", "VDFS", "SWUpdate", "SquashFS")
META_PATTERNS = {
    "platform": r"(?i)\bSAT-[A-Z0-9-]+WWC\b",
    "version_candidates": r"\b\d{4}\.\d{1,3}\b",
    "algorithms": r"(?i)\b(?:AES(?:[-_ ]?\d{3})?(?:[-_ ]?(?:CBC|GCM|CTR))?|SHA[-_ ]?(?:256|384|512)|RSA(?:[-_ ]?\d{4})?)\b",
    "release_type": r"\bSWU-[A-Z]{2,8}\b",
}
def inspect(path):
    with zipfile.ZipFile(path) as archive:
        info = archive.getinfo(ROOT + "info.txt")
        if info.file_size > 65536:
            raise ValueError("metadata exceeds limit")
        metadata = archive.read(info).decode("utf-8", errors="replace")
        safe_meta = {k: sorted(set(re.findall(p, metadata)))[:20]
                     for k, p in META_PATTERNS.items()}
        image = archive.getinfo(ROOT + "upgrade.msd")
        if not 0 < image.file_size <= MAX_IMAGE:
            raise ValueError("image outside expected size")
        digest = hashlib.sha256()
        samples = []
        # At most 16 one-MiB entropy samples spread throughout the image.
        indices = sorted({i * ((image.file_size - 1) // CHUNK) // 15 for i in range(16)})
        matches = Counter()
        previous = b""
        offset = 0
        head = b""
        with archive.open(image) as stream:
            while True:
                block = stream.read(CHUNK)
                if not block:
                    break
                if offset == 0:
                    head = block[:512]
                digest.update(block)
                if offset // CHUNK in indices:
                    freq = Counter(block)
                    entropy = -sum((n / len(block)) * math.log2(n / len(block)) for n in freq.values())
                    samples.append({"offset": offset, "entropy_bits_per_byte": round(entropy, 5)})
                # Count only fixed public keywords, no strings or bytes dumped.
                data = previous + block
                for token in TOKENS:
                    needle = token.encode()
                    matches[token] += data.count(needle) - previous.count(needle)
                previous = data[-32:]
                offset += len(block)
                if offset > MAX_IMAGE:
                    raise ValueError("image exceeds limit")
        if offset != image.file_size:
            raise ValueError("incomplete image")
        return {
            "platform": ROOT.split("/")[0],
            "metadata_tokens": safe_meta,
            "metadata_sha256": hashlib.sha256(archive.read(info)).hexdigest(),
            "image_size_bytes": offset,
            "image_sha256": digest.hexdigest(),
            "recognized_header_formats": [k for k, v in MAGICS.items() if head.startswith(v)],
            "entropy_samples": samples,
            "literal_keyword_counts": dict(matches),
            "limitations": [
                "High entropy cannot distinguish encryption from compression.",
                "Keyword matches can be incidental; absence is not evidence that a component is missing.",
                "Metadata tokens are candidates, not authenticated claims. No signature verification was performed.",
                "No firmware extraction, execution or device changes."
            ],
        }

def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fixture.zip"
        data = b"\x7fELF" + b"Linux Alexa " + b"\0" * (CHUNK + 3)
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(ROOT + "info.txt", "SAT-MT8532D24WWC 1071.0 AES-256-CBC SHA-512\nsecret=not-for-output")
            archive.writestr(ROOT + "upgrade.msd", data)
        result = inspect(path)
        assert result["image_sha256"] == hashlib.sha256(data).hexdigest()
        assert result["recognized_header_formats"] == ["ELF"]
        assert result["literal_keyword_counts"]["Alexa"] == 1
        assert result["metadata_tokens"]["version_candidates"] == ["1071.0"]
        assert "not-for-output" not in json.dumps(result)
        assert result["image_size_bytes"] == len(data)
        print("Synthetic fixture test passed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.archive:
        print(json.dumps(inspect(args.archive), indent=2))
    else:
        parser.error("provide archive or --self-test")
