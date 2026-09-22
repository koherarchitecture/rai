"""The three numbers on test sets never trained on: false presents, false absents, and how many honest answers reach counting.
With more than one test set, one threshold is chosen over all of them — the smallest margin that lets no non-counting answer
through anywhere — and each set is then reported at that threshold. usage:
    python scripts/eval_reader.py tests/testset-v1.jsonl [more.jsonl ...] [model] [--no-stem] [--show-misses]"""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.reader import Reader, BASE
from rai.kind import counts

paths = [a for a in sys.argv[1:] if a.endswith(".jsonl")] or ["tests/testset-v1.jsonl"]
model = next((a for a in sys.argv[1:] if not a.startswith("--") and not a.endswith(".jsonl")), BASE)
use_stem = "--no-stem" not in sys.argv
reader = Reader(model)

sets = {}
t0 = time.time(); n = 0
for p in paths:
    rows = [json.loads(l) for l in open(p)]
    for r in rows:
        span, margin = reader.read(r["question"], r["answer"], r["stem"] if use_stem else "")
        r["span"], r["margin"] = span, margin
    sets[p] = rows; n += len(rows)
secs = time.time() - t0

# the threshold: above every non-counting answer the reader found, in any set, rounded UP so the printed value can be
# pasted into rai/ask.py and still sit above them all
found_bad = [r["margin"] for rows in sets.values() for r in rows if not r["label"] and r["span"] and counts(r["answer"])]
threshold = math.ceil(max(found_bad) * 100) / 100 if found_bad else 0.0
hit = lambda r: r["span"] is not None and r["margin"] > threshold and counts(r["answer"])

print(f"{model}  stem={'on' if use_stem else 'off'}  rows={n}  {secs / n * 1000:.0f} ms/row")
print(f"threshold at zero false presents over {'both sets' if len(paths) == 2 else f'{len(paths)} set(s)'}: {threshold:.2f}")
for p, rows in sets.items():
    pos = [r for r in rows if r["label"]]; neg = [r for r in rows if not r["label"]]
    fp = sum(1 for r in neg if hit(r)); fn = sum(1 for r in pos if not hit(r))
    print(f"\n{p}")
    print(f"  false presents: {fp}/{len(neg)}   false absents: {fn}/{len(pos)}   honest answers counted: {len(pos) - fn}/{len(pos)}")
    for cls in sorted({r["class"] for r in rows}):
        rs = [r for r in rows if r["class"] == cls]
        ok = sum(1 for r in rs if hit(r) == r["label"])
        print(f"    {cls:13} {ok}/{len(rs)} right")
    if "--show-misses" in sys.argv:
        for r in pos:
            if not hit(r):
                print(f"    MISS {r['whole']}/{r['qid']:8} {r['answer']!r:55} -> {r['span']!r} {r['margin']:.2f}")
