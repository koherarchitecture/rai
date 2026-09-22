"""The three numbers, on a test set never trained on: false presents, false absents, and how many honest answers reach counting.
usage: python scripts/eval_reader.py tests/testset-v1.jsonl [model] [--no-stem]"""
import json, math, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.reader import Reader, BASE
from rai.kind import counts

path = sys.argv[1]
model = next((a for a in sys.argv[2:] if not a.startswith("--")), BASE)
use_stem = "--no-stem" not in sys.argv
rows = [json.loads(l) for l in open(path)]
reader = Reader(model)

t0 = time.time()
for r in rows:
    span, margin = reader.read(r["question"], r["answer"], r["stem"] if use_stem else "")
    r["span"], r["margin"] = span, margin
secs = time.time() - t0

# choose the threshold on this set at zero false presents: the smallest margin above every found non-counting answer
found_bad = [r["margin"] for r in rows if not r["label"] and r["span"] and counts(r["answer"])]
# rounded UP, so the printed value can be pasted into rai/ask.py and still sits above every found non-counting answer
threshold = math.ceil(max(found_bad) * 100) / 100 if found_bad else 0.0
pos = [r for r in rows if r["label"]]
neg = [r for r in rows if not r["label"]]
fp = sum(1 for r in neg if r["span"] and r["margin"] > threshold and counts(r["answer"]))
fn = sum(1 for r in pos if not (r["span"] and r["margin"] > threshold and counts(r["answer"])))
print(f"{model}  stem={'on' if use_stem else 'off'}  rows={len(rows)}  {secs/len(rows)*1000:.0f} ms/row")
print(f"threshold at zero false presents: {threshold:.2f}")
print(f"false presents: {fp}/{len(neg)}   false absents: {fn}/{len(pos)}   honest answers counted: {len(pos)-fn}/{len(pos)}")
for cls in sorted({r['class'] for r in rows}):
    rs = [r for r in rows if r["class"] == cls]
    ok = sum(1 for r in rs if ((r["span"] is not None and r["margin"] > threshold and counts(r["answer"])) == r["label"]))
    print(f"  {cls:13} {ok}/{len(rs)} right")
if "--show-misses" in sys.argv:
    for r in pos:
        if not (r["span"] and r["margin"] > threshold and counts(r["answer"])):
            print(f"  MISS {r['whole']}/{r['qid']:8} {r['answer']!r:60} -> {r['span']!r} {r['margin']:.2f}")
