#!/usr/bin/env bash
# The full 0.3.8 recipe, in four steps. 0.3.8 is the weights of 0.3.7 and of a reader taught Hinglish, averaged 0.4 and 0.6.
#  1. 0.3.7: deepset's MiniLM trained on 29,000 rows (data/train-synth.jsonl), seeds 7, 1 and 2, the three averaged.
#  2. The teacher: HingBERT (l3cube-pune/hing-bert, BERT-base further trained on romanised Hinglish, CC-BY-4.0) taught SQuAD 2.0
#     (scripts/squad_rows.py) and then the same rows with 5,800 Hinglish ones (data/train-hinglish.jsonl), seed 7. It is 110M parameters
#     and needs a GPU with about 20 GB free.
#  3. The Hinglish reader: deepset's MiniLM on the same rows, learning the teacher's scores on the Hinglish rows (scripts/distil.py),
#     seeds 7, 1 and 2, averaged. It reads Hinglish twice as well as 0.3.7 and Indian names a quarter worse.
#  4. 0.3.8: 0.4 of step 1 and 0.6 of step 3 (scripts/blend.py), which keeps nearly all of 0.3.7's names and most of the Hinglish.
# PYTHON picks the interpreter (default python3); install requirements.txt first.
set -eu
cd "$(dirname "$0")/.."
P=${PYTHON:-python3}
$P scripts/synth_hinglish.py 5800
$P scripts/squad_rows.py
$P tests/test_vegan.py   # train only on rows that name no animal product
for s in 7 1 2; do
  $P -m rai.train --data data/train-synth.jsonl --out runs/rai-0.3.7-seed$s --epochs 2 --batch 32 --seed $s
done
$P scripts/soup.py runs/rai-0.3.7 runs/rai-0.3.7-seed7 runs/rai-0.3.7-seed1 runs/rai-0.3.7-seed2
cat data/train-synth.jsonl data/train-hinglish.jsonl > data/train-0.3.8.jsonl
$P -m rai.train --base l3cube-pune/hing-bert --data data/squad2-train.jsonl --out runs/teacher-squad --epochs 2 --lr 3e-5 --batch 32
$P -m rai.train --base runs/teacher-squad --data data/train-0.3.8.jsonl --out runs/teacher --epochs 2 --batch 32 --seed 7
for s in 7 1 2; do
  $P scripts/distil.py --teacher runs/teacher --out runs/rai-hinglish-seed$s --seed $s
done
$P scripts/soup.py runs/rai-hinglish runs/rai-hinglish-seed7 runs/rai-hinglish-seed1 runs/rai-hinglish-seed2
$P scripts/blend.py runs/rai-0.3.7 runs/rai-hinglish 0.6 runs/rai-0.3.8
$P tests/test_reader_v03.py runs/rai-0.3.8
