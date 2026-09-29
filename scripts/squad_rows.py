"""SQuAD 2.0 as pointing rows for rai.train, with every row that names an animal product left out.
SQuAD 2.0 (Rajpurkar et al. 2018, CC BY-SA 4.0): Wikipedia passages, questions written by paid crowdworkers, and 43,498 unanswerable ones
written to look answerable. It teaches where an answer ends and a plausible non-answer begins. Admitted 25 Sep 2026 (koher/debt-resolution-20260923.md).
usage: python scripts/squad_rows.py        writes data/squad2-train.jsonl"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "tests"))
from test_vegan import ANIMAL, ALLOWED

URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json"
vegan = lambda text: not ANIMAL.search(ALLOWED.sub("", text))
kept = dropped = 0
with urllib.request.urlopen(URL, timeout=300) as r:
    data = json.load(r)["data"]
with open(os.path.join(HERE, "data", "squad2-train.jsonl"), "w") as out:
    for article in data:
        for para in article["paragraphs"]:
            if not vegan(para["context"]):
                dropped += len(para["qas"]); continue
            for qa in para["qas"]:
                if not qa["question"].strip() or len(qa["question"]) > 250:   # one SQuAD "question" is ~1,000 spaces, longer than the window (27 Sep 2026)
                    dropped += 1; continue
                span = "" if qa["is_impossible"] else qa["answers"][0]["text"]
                if not vegan(qa["question"]) or not vegan(span):
                    dropped += 1; continue
                out.write(json.dumps({"question": qa["question"], "stem": "", "answer": para["context"], "span": span}) + "\n")
                kept += 1
print(f"{kept:,} rows kept, {dropped:,} left out as naming an animal product")
