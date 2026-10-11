#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
mkdir -p "$ROOT_DIR/book/build" "$ROOT_DIR/dist"
cd "$ROOT_DIR/book"
for pass in 1 2 3; do
  xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory=build main.tex > "build/pass-$pass.stdout"
done
cp build/main.pdf ../dist/ai-self-study.pdf
printf 'PDF built: %s\n' "$ROOT_DIR/dist/ai-self-study.pdf"
