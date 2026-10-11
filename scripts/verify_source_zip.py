#!/usr/bin/env python3
"""Verify manifest, rebuild PDF, run tests and reproduce experiments from a ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import os
import re
import subprocess
import tempfile
import zipfile
import fitz


def pdf_content(path):
    with fitz.open(path) as pdf:
        pages = [{"text_sha256": hashlib.sha256(p.get_text().encode()).hexdigest(),
                  "pixel_sha256": hashlib.sha256(p.get_pixmap(alpha=False).samples).hexdigest()}
                 for p in pdf]
        links = [[{"kind": x["kind"], "page": x.get("page"), "uri": x.get("uri"),
                   "nameddest": x.get("nameddest")} for x in p.get_links()] for p in pdf]
        return {"pages": pages, "toc": pdf.get_toc(), "links": links}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve()
    with tempfile.TemporaryDirectory(prefix="ai-source-rebuild-") as tmp:
        temp = Path(tmp)
        with zipfile.ZipFile(archive) as z:
            for member in z.infolist():
                if member.is_dir():
                    continue
                target = (temp / member.filename).resolve()
                if not target.is_relative_to(temp) or member.external_attr >> 16 & 0o170000 == 0o120000:
                    raise ValueError("Unsafe archive member")
            z.extractall(temp)
        root = temp / "ai-self-study"
        manifest = json.loads((root / "SOURCE-MANIFEST.json").read_text())
        for name, expected in manifest["files"].items():
            path = (root / name).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != expected["sha256"]:
                raise ValueError(f"Manifest mismatch: {name}")
        delivered = pdf_content(root / "dist/ai-self-study.pdf")
        subprocess.run(["bash", "scripts/build_pdf.sh"], cwd=root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        rebuilt = pdf_content(root / "dist/ai-self-study.pdf")
        assert delivered == rebuilt, "PDF text, pixels, bookmarks or links changed"
        test_run = subprocess.run(["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
                       cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
        subprocess.run(["python", "experiments/run_all.py", "--out", str(temp / "rerun")],
                       cwd=root, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert (root / "results/metrics.json").read_bytes() == (temp / "rerun/metrics.json").read_bytes(), "Original experiments differ from reference"
        for name, extra in [("attention_walkthrough", []), ("residual_debug", ["--seed", "19"]), ("micro_research", [])]:
            out = temp / name
            subprocess.run(["python", "experiments/run_all.py", "--experiment", name,
                            "--out", str(out)] + extra, cwd=root, env=env, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            assert (root / "results" / name / "metrics.json").read_bytes() == (out / "metrics.json").read_bytes(), f"New experiment differs: {name}"
        generated = {p.relative_to(root): p.read_bytes() for p in (root / "book/generated").glob("v02-*.tex")}
        generated[Path("research/micro-study-v02.md")] = (root / "research/micro-study-v02.md").read_bytes()
        subprocess.run(["python", "scripts/write_v02_results.py"], cwd=root, env=env, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert all((root / p).read_bytes() == data for p, data in generated.items()), "Numeric fragments are not generated from delivered results"
        test_count = int(re.search(rb"Ran (\d+) tests", test_run.stdout).group(1))
        report = {"status": "PASS", "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                  "manifest_files": len(manifest["files"]), "pages": len(rebuilt["pages"]),
                  "pdf_text_pixels_toc_links_identical": True,
                  "tests": f"{test_count} passed", "experiments": "original 7 + attention/residual/15-run microstudy; exact JSON match in this environment",
                  "numeric_fragments_regenerated_identically": True,
                  "comparison_scope": "same XeLaTeX/fonts, Python/NumPy and one-thread CPU environment"}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
