#!/bin/sh

set -o errexit
set -o nounset

srcDir="testproject"
outDir="build-sphinx-testproject"

echo "Building 'testproject' with postpocessing disabled..."
rm -rf "$outDir"
sphinx-build -a "$srcDir" "$outDir"

echo "[runtest.sh] Check <table> tags"
grep -q '<table' "$outDir/index.html"    && true
grep -q '<table' "$outDir/excluded.html" && true

echo "[runtest.sh] Check that stylesheet is copied"
[ -f "$outDir/_static/divparams.css" ]

echo "[runtest.sh] Building 'testproject' with postpocessing enabled..."
rm -rf "$outDir"
sphinx-build -a -D divparams_enable_postprocessing=True "$srcDir" "$outDir"

echo "[runtest.sh] Check <table> tags"
grep -q '<table' "$outDir/index.html"    || true
grep -q '<table' "$outDir/excluded.html" && true


echo "[runtest.sh] Check that stylesheet is copied"
[ -f "$outDir/_static/divparams.css" ]

echo "[runtest.sh] All tests passed."
