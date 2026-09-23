#!/usr/bin/env bash
# The full 0.3.1 training recipe, on CPU: 12,000 rows x 2 epochs, batch 32. About 8 minutes on 18 ARM cores, nearer an hour on 5 laptop cores.
# PYTHON picks the interpreter (default python3); install requirements.txt into it first.
# It continues from deepset's weights, not from runs/rai-0.3, so the result is one clean recipe rather than a chain.
set -e
cd "$(dirname "$0")/.."
P=${PYTHON:-python3}
$P scripts/synth.py 200
$P -m rai.train --data data/train-synth.jsonl --out runs/rai-0.3.5 --epochs 2 --batch 32
$P tests/test_reader_v03.py runs/rai-0.3.5
