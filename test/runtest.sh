#!/bin/bash

set -o errexit
set -o nounset

srcDir="testproject"
outDir="build-sphinx-testproject"

echo "Building 'testproject' with postpocessing disabled..."
rm -rf "$outDir"
sphinx-build -a "$srcDir" "$outDir"

echo "[runtest.sh] Check <table> tags"
[ "$(grep -c '<table' $outDir/index.html    || true)" = "1" ]
[ "$(grep -c '<table' $outDir/test2.html    || true)" = "1" ]
[ "$(grep -c '<table' $outDir/excluded.html || true)" = "1" ]

echo "[runtest.sh] Check 'divparams' classes"
[ "$(grep -c 'divparams-list' $outDir/index.html    || true)" = "0" ]
[ "$(grep -c 'divparams-list' $outDir/test2.html    || true)" = "0" ]
[ "$(grep -c 'divparams-list' $outDir/excluded.html || true)" = "0" ]

echo "[runtest.sh] Check linebreaks"
[ "$(grep -c '<br' $outDir/index.html    || true)" = "0" ]
[ "$(grep -c '<br' $outDir/test2.html    || true)" = "0" ]
[ "$(grep -c '<br' $outDir/excluded.html || true)" = "0" ]

echo "[runtest.sh] Check that stylesheet is copied"
[ -f "$outDir/_static/divparams.css" ]

echo "[runtest.sh] Building 'testproject' with postpocessing enabled..."
rm -rf "$outDir"
sphinx-build -a -D divparams_enable_postprocessing=1 "$srcDir" "$outDir"

echo "[runtest.sh] Check <table> tags"
[ "$(grep -c '<table' $outDir/index.html    || true)" = "0" ]
[ "$(grep -c '<table' $outDir/test2.html    || true)" = "0" ]
[ "$(grep -c '<table' $outDir/excluded.html || true)" = "1" ]

echo "[runtest.sh] Check 'divparams' classes"
[ "$(grep -c 'divparams-list' $outDir/index.html    || true)" = "1" ]
[ "$(grep -c 'divparams-list' $outDir/test2.html    || true)" = "1" ]
[ "$(grep -c 'divparams-list' $outDir/excluded.html || true)" = "0" ]

echo "[runtest.sh] Check linebreaks"
[ "$(grep -c '<br' $outDir/index.html    || true)" = "2" ]
[ "$(grep -c '<br' $outDir/test2.html    || true)" = "2" ]
[ "$(grep -c '<br' $outDir/excluded.html || true)" = "0" ]

echo "[runtest.sh] Check that stylesheet is copied"
[ -f "$outDir/_static/divparams.css" ]

echo "[runtest.sh] All tests passed."
