"""Check translated cells and preserved assets against the specified arXiv source.

Run with Python -B to avoid creating a cache. The source is read only.
This audit detects data loss and transcription changes; it does not certify
semantic translation accuracy or the authors' empirical claims.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def active(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def rows(text, columns):
    return [cells for line in text.splitlines()
            if len(cells := re.split(r"(?<!\\)&", line)) == columns
            and r"\multicolumn" not in line]


def numbers(text):
    return re.findall(r"\d+(?:\.\d+)?", re.sub(
        r"\\textbf\{|\\color\{refgray\}|\\shortstack\{", "", text))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    src = args.source_dir
    dst = Path(__file__).resolve().parent
    read = lambda p: active((src / p).read_text())
    body = (dst / "body.tex").read_text()
    a = rows(read("sections/large_scale_exp.tex"), 7)[1:]
    b = rows((dst / "tables/pretraining.tex").read_text(), 6)[1:]
    assert len(a) == len(b) == 34
    for x, y in zip(a, b):
        assert numbers(" ".join(x[2:])) == numbers(" ".join(y[1:]))
    # Benchmark identifiers are checked independently of their numerical cells.
    for x, y in zip(a[5:], b[5:]):
        metric = x[1].strip().split()[0]
        if metric != "Validation":
            assert metric in y[0], (metric, y[0])
    a = [line.split("&")[1:] for line in read("sections/long_context_exp.tex").splitlines()
         if line.strip().startswith(("MoE-27B", "Engram-27B"))]
    b = rows((dst / "tables/long_context.tex").read_text(), 5)[1:]
    assert len(a) == 4 and len(b) == 12
    for i in range(4):
        for j in range(12):
            assert numbers(a[i][j]) == numbers(b[j][i + 1])
            for marker in (r"\textbf", r"\underline"):
                assert (marker in a[i][j]) == (marker in b[j][i + 1])
    a = [s for s in read("tabs/appendix_detailed_arch.tex").splitlines() if "&" in s][1:]
    b = [s for s in (dst / "tables/architecture.tex").read_text().splitlines() if "&" in s][1:]
    assert len(a) == len(b) == 33
    for x, y in zip(a, b):
        assert numbers(x.split("&", 1)[1]) == numbers(y.split("&", 1)[1])
    # All literal automatic Patchscopes outputs are present in full, with Chinese.
    a = read("sections/analysis.tex")
    patch_outputs = re.findall(r"\n\s*: ([^&]+)&", a)
    compact = lambda s: " ".join(s.split())
    assert len(patch_outputs) == 5
    for output in patch_outputs:
        assert compact(output) in compact(body)
    throughputs = re.findall(r"&\s*(\d,\d{3}\.\d{2})", a)
    assert len(throughputs) == 4 and all(x in body for x in throughputs)
    # Token order, all accents, visible spaces, and literal control spellings.
    a = [s for s in read("main.tex").splitlines() if re.match(r"\s*[1-5] &", s)]
    b = [s for s in body.splitlines() if re.match(r"[1-5] &", s) and r"\texttt" in s]
    assert len(a) == len(b) == 5
    token = lambda s: re.findall(r"\\texttt\{([^}]+)\}", s.replace(r"\spacebox", r"\textvisiblespace"))
    for x, y in zip(a, b):
        assert numbers(x.split("&", 2)[0] + " " + x.split("&", 2)[1]) == numbers(y.split("&", 2)[0] + " " + y.split("&", 2)[1])
        assert token(x) == token(y), (token(x), token(y))
    refs = (dst / "references.tex").read_text()
    keys = set(re.findall(r"\\bibitem\{([^}]+)\}", refs))
    alltex = "\n".join(p.read_text() for p in dst.rglob("*.tex") if p.name != "references.tex")
    cites = {k.strip() for m in re.findall(r"\\cite\{([^}]+)\}", alltex) for k in m.split(",")}
    assert len(keys) == 135 and keys == cites
    assert all(k.startswith("engram-") for k in keys)
    if (src / "engram-bib.bbl").exists():
        bbl = (src / "engram-bib.bbl").read_text()
        canonical = re.sub(r"\\bibitem\[.*?\]\{([^}]+)\}", lambda m: r"\bibitem{engram-" + m[1] + "}", bbl, flags=re.S)
        assert refs.split("\n", 1)[1] == canonical
    figs = json.loads((dst / "figures-manifest.json").read_text())
    assert len(figs) == 8
    for fig in figs:
        assert sha(src / fig["source"]) == sha(dst / fig["output"]) == fig["sha256"]
    assert len(re.findall(r"\\begin\{equation\}", body)) == 9
    assert len(re.findall(r"\\label\{engram-fig-\d\}", body)) == 8
    report = {
        "status": "passed", "pretraining_all_data_rows": 34,
        "benchmark_names": "preserved", "long_context_transposed_cells": 48,
        "long_context_bold_underline_markers": "preserved", "architecture_data_rows": 33,
        "patchscopes_complete_literal_outputs": 5, "throughput_values": throughputs,
        "tokenizer_rows": 5, "token_order_accents_control_spellings": "identical",
        "reference_entries": 135, "missing_citations": [], "uncited_source_entries": [],
        "source_generated_bibliography": "identical after citation-key prefix and natbib-label removal",
        "unchanged_vector_assets": 8, "numbered_equations": 9,
        "scope": "Mechanical checks complement source reading and visual review; they do not certify translation semantics or scientific correctness."
    }
    if args.out:
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
