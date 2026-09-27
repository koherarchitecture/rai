#!/usr/bin/env bash
# Builds rai-server.tar for CapRover from rai's code and its CURRENT reader only (READER in rai/ask.py). Run from anywhere.
# Deploy: caprover deploy -n <server> -a <app> -t deploy/rai-server.tar   (then set RAI_API_KEY in the app's environment)
set -eu
cd "$(dirname "$0")/.."
reader=$(python3 -c "import re;print(re.search(r'\"runs\", \"([^\"]+)\"', open('rai/ask.py').read()).group(1))")
tmp=$(mktemp -d)
mkdir -p "$tmp/rai" "$tmp/runs"
cp deploy/Dockerfile deploy/captain-definition "$tmp/"
cp rai/*.py "$tmp/rai/"
cp -R "runs/$reader" "$tmp/runs/"
rm -f "$tmp/runs/$reader/results"*.json
tar -cf deploy/rai-server.tar -C "$tmp" .
rm -r "$tmp"
echo "deploy/rai-server.tar: reader $reader, $(du -h deploy/rai-server.tar | cut -f1)"
