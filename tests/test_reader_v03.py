"""0.3.0 does one thing more than 0.2.0: the trained reader finds honest bare answers that the untrained one refused,
still at zero false presents on test set v1, which it never saw. Run: python tests/test_reader_v03.py runs/rai-0.3-full"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math
from test_reader_v02 import numbers, ROWS
from rai.ask import THRESHOLD
from rai.kind import counts

FLOOR_0_2 = 16   # honest answers counted by 0.2.0 on test set v1

if __name__ == "__main__":
    run = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "rai-0.3-full")
    if not os.path.exists(os.path.join(run, "config.json")):
        print(f"no trained reader at {run}; run the training first"); sys.exit(0)
    th, fp, honest, npos, nneg = numbers(run)
    th = math.ceil(th * 100) / 100   # the value to paste into rai/ask.py: rounded up, never down
    print(f"{run}: threshold {th:.2f}  false presents {fp}/{nneg}  honest counted {honest}/{npos}  (0.2.0: {FLOOR_0_2}/{npos})")
    assert fp == 0, "a false present turns not-complete into complete"
    assert honest > FLOOR_0_2, "0.3.0 must find more honest answers than 0.2.0 at zero false presents"
    shipped = sum(1 for r in ROWS if not r["label"] and r["span"] is not None and r["margin"] > THRESHOLD and counts(r["answer"]))
    assert shipped == 0, f"rai/ask.py THRESHOLD {THRESHOLD} lets {shipped} non-counting answer(s) through; set it to {th:.2f}"
    print("ok 0.3.0: does more than 0.2.0 by", honest - FLOOR_0_2, "honest answers; the shipped threshold", THRESHOLD, "passes no non-counting answer")
