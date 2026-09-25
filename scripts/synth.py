"""100% synthetic training pairs, labels by construction. Writes data/train-synth.jsonl.
Row: question, stem, answer, span (the phrase that answers, or null), class. Templates only, seeded; every particular is a plain real thing.
Rewritten 22 September 2026: fillers are written PER QUESTION and phrased to follow that question's stem, after ten sampled rows showed
a keyword map handing "The wallet." to "What did you do while you waited?" as a counting answer. A filler that does not answer its question
is a wrong label, and a wrong label teaches the hollow-present error the tally exists to refuse.
0.3.5, 23 September 2026: eight more forms; three rows in ten read without their stem; every tests/testset*.jsonl is held out; and no
training question may repeat a question from tests/unseen-forms/, which the reader never sees.
0.3.6, 25 September 2026: every filler and every evasive, deferred and general reply is Comma's (data/fill-comma.jsonl, data/nonanswers-comma.jsonl).
usage: python scripts/synth.py [rows_per_question=200]"""
import json, os, random, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
PER_Q = int(sys.argv[1]) if len(sys.argv) > 1 else 200

# questions of one whole whose answers can legitimately swap: never used as off-question pairs for each other
EXCHANGEABLE = [{"pocket/oldest", "pocket/heaviest", "pocket/miss"}, {"handful/biggest", "handful/smallest"}, {"queue/long", "wait/long", "walk/time", "tea/time"}, {"artwork/where", "artwork/history"},
                {"call/about", "call/who"}, {"call/ended", "call/first"}, {"repair/worked", "repair/wrong"}, {"repair/first", "repair/used"}, {"lost/checked", "lost/found", "lost/last"}, {"ride/ends", "ride/route"}, {"door/colour", "door/material"}, {"door/behind", "door/stuck"}, {"screen/corner", "screen/dock", "screen/most", "screen/never"}]

EMPTY = ["", "-", "?", "yes", "ok", "hm"]

# 0.3.6, 25 September 2026: every filler (whole/qid -> phrases that answer that question and read after its stem) and every evasive, deferred
# and general reply was written by Comma v0.1, a model trained only on openly licensed text, and each was read and judged before it was kept.
# The words 0.3.5 trained on are in this file's history. EMPTY stays: marks and single words have no author.
FILL = {c["key"]: c["fill"] for c in map(json.loads, open(os.path.join(HERE, "data", "fill-comma.jsonl")))}
NON = [json.loads(l) for l in open(os.path.join(HERE, "data", "nonanswers-comma.jsonl"))]
EVASIVE, DEFERRED, GENERAL = ([n["reply"] for n in NON if n["kind"] == k] for k in ("evasive", "deferred", "general"))

# Held out: no phrase in the test set may appear in training, in any class. Until 22 September 2026 153 of the test set's
# 180 honest answers were also training fillers, so the reader was scored partly on recall. Refused here, and checked at the end.
norm = lambda t: t.strip().lower().rstrip(".")
HELD = {norm(json.loads(l)["answer"]) for t in glob.glob(os.path.join(HERE, "tests", "testset*.jsonl")) for l in open(t)}   # every test set, the unseen-forms one included
EVASIVE, DEFERRED, GENERAL = ([a for a in L if norm(a) not in HELD] for L in (EVASIVE, DEFERRED, GENERAL))

qs = {}
for path in sorted(glob.glob(os.path.join(HERE, "wholes", "*.yaml"))):
    w = load_whole(path)
    for q in w["questions"]:
        qs[f"{os.path.basename(path)[:-5]}/{q['id']}"] = q
# 0.3.5: the forms in tests/unseen-forms/ are never trained on, so a reader can be measured on questions it has not seen
qnorm = lambda t: t.strip().lower().rstrip("?")
unseen = {qnorm(q["text"]) for p in glob.glob(os.path.join(HERE, "tests", "unseen-forms", "*.yaml")) for q in load_whole(p)["questions"]}
if any(qnorm(q["text"]) in unseen for q in qs.values()):
    raise SystemExit(f"a training question repeats an unseen form's question: {[k for k, q in qs.items() if qnorm(q['text']) in unseen]}")
missing = [k for k in qs if k not in FILL]
if missing:
    raise SystemExit(f"no fillers for {missing}; every question needs its own")
# a filler is held out if it, or the stem read out before it (a restating row), is a test answer
FILL = {k: [a for a in v if norm(a) not in HELD and norm(qs[k]["stem"] + a) not in HELD] for k, v in FILL.items() if k in qs}
if not all(FILL.values()):
    raise SystemExit(f"holding out the test set left no fillers for {[k for k, v in FILL.items() if not v]}")


def swappable(a, b):
    return any(a in g and b in g for g in EXCHANGEABLE)


rows = []
for key, q in qs.items():
    f = FILL[key]
    others = [k for k in qs if k.split("/")[0] == key.split("/")[0] and k != key and not swappable(k, key)]
    for _ in range(PER_Q):
        r = random.random()
        if r < 0.40:                                   # bare particular, as people say it
            a = random.choice(f); ans = a[0].upper() + a[1:] + "."
            rows.append(dict(question=q["text"], stem=q["stem"], answer=ans, span=a, cls="bare"))
        elif r < 0.50:                                 # restating particular: the stem read out, then the answer
            a = random.choice(f); ans = q["stem"] + a + "."
            rows.append(dict(question=q["text"], stem="", answer=ans, span=a, cls="restating"))
        elif r < 0.65:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(EVASIVE), span=None, cls="evasive"))
        elif r < 0.75:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(DEFERRED), span=None, cls="deferred"))
        elif r < 0.85:                                 # off-question: a real answer to a different, non-swappable question of the same whole
            o = random.choice(others); a = random.choice(FILL[o]); ans = a[0].upper() + a[1:] + "."
            rows.append(dict(question=q["text"], stem=q["stem"], answer=ans, span=None, cls="off-question"))
        elif r < 0.90:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(EMPTY), span=None, cls="empty"))
        else:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(GENERAL), span=None, cls="general"))

# 0.3.5: forms people write often carry no stem, so three rows in ten are read without one, in every class alike, so a missing stem is never itself a cue
for r in rows:
    if r["stem"] and random.random() < 0.3:
        r["stem"] = ""

leak = [r["answer"] for r in rows if norm(r["answer"]) in HELD or (r["span"] and norm(r["span"]) in HELD)]
if leak:
    raise SystemExit(f"{len(leak)} training rows repeat the test set, e.g. {leak[0]!r}")
random.shuffle(rows)
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
out = os.path.join(HERE, "data", "train-synth.jsonl")
with open(out, "w") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "rows", dict(Counter(r["cls"] for r in rows)), "->", out)
