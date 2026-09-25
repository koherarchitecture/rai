#!/usr/bin/env bash
# The full 0.3.6 recipe, on CPU: 23,200 rows x 2 epochs, batch 32, pointed three times with seeds 7, 1 and 2, then the three averaged into one reader.
# About 25 minutes a seed on 4 ARM cores; the three run one after another here. PYTHON picks the interpreter (default python3); install requirements.txt into it first.
# Each continues from deepset's weights, not from an earlier rai, so the result is one clean recipe rather than a chain.
set -e
cd "$(dirname "$0")/.."
P=${PYTHON:-python3}
$P scripts/synth.py 200
for s in 7 1 2; do
  $P -m rai.train --data data/train-synth.jsonl --out runs/rai-0.3.6-seed$s --epochs 2 --batch 32 --seed $s
done
$P scripts/soup.py runs/rai-0.3.6 runs/rai-0.3.6-seed7 runs/rai-0.3.6-seed1 runs/rai-0.3.6-seed2
$P tests/test_reader_v03.py runs/rai-0.3.6
