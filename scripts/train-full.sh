#!/usr/bin/env bash
# The full 0.3.7 recipe: 0.3.6's 23,200 rows (data/train-synth-0.3.6.jsonl, made by scripts/synth.py) and 5,800 rows of
# questions as people write them (data/train-live.jsonl, made by scripts/synth_live.py 5800), shuffled together with seed 37
# into data/train-synth.jsonl; 2 epochs, batch 32, pointed three times with seeds 7, 1 and 2, the three averaged into one reader.
# About 3 minutes a seed on a Mac's GPU, about 25 on 4 ARM cores. PYTHON picks the interpreter (default python3); install requirements.txt first.
# Each continues from deepset's weights, not from an earlier rai, so the result is one clean recipe rather than a chain.
set -eu
cd "$(dirname "$0")/.."
P=${PYTHON:-python3}
$P scripts/synth_live.py 5800
$P - <<'PY'
import random
random.seed(37)
rows = open("data/train-synth-0.3.6.jsonl").read().splitlines() + open("data/train-live.jsonl").read().splitlines()
random.shuffle(rows)
open("data/train-synth.jsonl", "w").write("\n".join(rows) + "\n")
PY
$P tests/test_vegan.py   # train only on rows that name no animal product
for s in 7 1 2; do
  $P -m rai.train --data data/train-synth.jsonl --out runs/rai-0.3.7-seed$s --epochs 2 --batch 32 --seed $s
done
$P scripts/soup.py runs/rai-0.3.7 runs/rai-0.3.7-seed7 runs/rai-0.3.7-seed1 runs/rai-0.3.7-seed2
$P tests/test_reader_v03.py runs/rai-0.3.7
