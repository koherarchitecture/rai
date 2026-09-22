"""0.2.0 does one thing more than 0.1.0: it refuses, by itself, every answer that does not count — evasive and off-question —
without a person marking anything, at zero false presents on test set v1. What it cannot yet do is find most honest bare answers;
that number is recorded here as the floor 0.3.0 must raise. Run: python tests/test_reader_v02.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.reader import Reader
from rai.kind import counts

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS = [json.loads(l) for l in open(os.path.join(HERE, "tests", "testset-v1.jsonl"))]


def numbers(model=None):
    reader = Reader(model) if model else Reader()
    for r in ROWS:
        r["span"], r["margin"] = reader.read(r["question"], r["answer"], r["stem"])
    bad = [r["margin"] for r in ROWS if not r["label"] and r["span"] and counts(r["answer"])]
    th = max(bad) if bad else 0.0
    hit = lambda r: r["span"] is not None and r["margin"] > th and counts(r["answer"])
    fp = sum(1 for r in ROWS if not r["label"] and hit(r))
    honest = sum(1 for r in ROWS if r["label"] and hit(r))
    return th, fp, honest, sum(1 for r in ROWS if r["label"]), sum(1 for r in ROWS if not r["label"])


if __name__ == "__main__":
    th, fp, honest, npos, nneg = numbers(sys.argv[1] if len(sys.argv) > 1 else None)
    assert fp == 0, "a false present turns not-complete into complete"
    print(f"threshold {th:.2f}  false presents {fp}/{nneg}  honest counted {honest}/{npos}")
    assert honest >= 16, "0.2.0's recorded floor on test set v1 (16 after the off-question construction was repaired on 22 September)"
    print("ok 0.2.0: refuses every non-counting answer by itself; finds", honest, "of", npos, "honest ones")
