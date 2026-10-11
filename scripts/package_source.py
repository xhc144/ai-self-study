#!/usr/bin/env python3
"""Package the public educational project using an explicit file allowlist."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = [
    "book/chapters", "book/generated", "docs", "experiments", "licenses",
    "qa", "research", "results", "scripts", "tests",
]
ROOT_FILES = [
    ".gitignore", "LICENSE", "README.md", "requirements.txt",
    "requirements-build.txt", "book/main.tex", "book/references.tex",
    "dist/ai-self-study.pdf",
]


def main():
    paths = [ROOT / name for name in ROOT_FILES]
    for folder in DIRECTORIES:
        paths.extend(p for p in (ROOT / folder).rglob("*") if p.is_file()
                     and not any(part in {"__pycache__", "render", "style-check"}
                                 for part in p.relative_to(ROOT).parts)
                     and p.suffix != ".pyc")
    paths = sorted(set(paths))
    if any(not p.is_file() for p in paths):
        raise FileNotFoundError("An explicitly required delivery file is missing")
    files = {p.relative_to(ROOT).as_posix(): {
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        "size_bytes": p.stat().st_size,
    } for p in paths}
    manifest = json.dumps({"format": 1, "release": "0.2.1", "files": files},
                          ensure_ascii=False, indent=2).encode() + b"\n"
    out = ROOT / "dist/ai-self-study-source.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        def add(name, data):
            item = zipfile.ZipInfo("ai-self-study/" + name,
                                   date_time=(2026, 10, 11, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o100644 << 16
            z.writestr(item, data)
        for p in paths:
            add(p.relative_to(ROOT).as_posix(), p.read_bytes())
        add("SOURCE-MANIFEST.json", manifest)
    (ROOT / "dist/source-manifest.json").write_bytes(manifest)
    print(json.dumps({"archive": str(out), "files": len(files),
                      "size_bytes": out.stat().st_size,
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
