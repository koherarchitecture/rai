"""No text rai is trained or tested on names an animal product (Koher policy, 23 September 2026).
Scans the forms, the scripts that write the data, the training data and every test set, and fails on any match.
Plant milks (soy, oat, almond, coconut, rice, plant) and peanut butter are allowed.
The pretraining corpus (data/pretrain/, data/selected*/, over a gigabyte) is scanned once, when it is compiled: a clean scan records each
file's sha256 in vegan-scanned.json beside it, and every later run only checks that each file still has the fingerprint it was scanned with.
A corpus file that changed, or was never scanned, fails.
usage: python tests/test_vegan.py             the forms, scripts, data and tests in full; the corpus by fingerprint (seconds)
       python tests/test_vegan.py --corpus    scan the corpus in full and record the clean files (about 80 s on the Mac, 12 min on the ThinkPad)"""
import glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = r"milk|milky|dairy|curd|dahi|ghee|paneer|butter|buttermilk|chaas|lassi|cream|cheese|yogh?urt|eggs?|omelettes?|meat|chicken|mutton|beef|pork|bacon|ham|fish|prawns?|shrimps?|crabs?|honey|leather|wool|woollen|silk|suede|fur|feathers?|gelatine?|lard|malai|kheer|khoya|mawa|rabdi|pearls?|ivory|beeswax|lanolin|shellac|mayonnaise|mayo"
ANIMAL = re.compile(rf"\b({WORDS})\b", re.I)
ALLOWED = re.compile(r"\b(soy|oat|almond|coconut|rice|plant) milk\b|\bpeanut butter\b", re.I)
FILES = ["wholes/*.yaml", "wholes/*.md", "tests/unseen-forms/*.yaml", "notions/*.yaml", "scripts/*.py", "data/*.jsonl", "tests/testset*.jsonl"]
CORPUS = ["data/pretrain*/*.txt", "data/selected*/*.txt"]  # data/pretrain-big/ too (25 Sep 2026)


def files(patterns):
    return [p for pattern in patterns for p in sorted(glob.glob(os.path.join(HERE, pattern)))]


def scan(path):
    return [f"{os.path.relpath(path, HERE)}:{n}: {m.group(0)}"
            for n, line in enumerate(open(path, encoding="utf-8"), 1) for m in ANIMAL.finditer(ALLOWED.sub("", line))]


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def stamp_of(path):
    return os.path.join(os.path.dirname(path), "vegan-scanned.json")


def scan_corpus():
    """Scan every corpus file in full and record the clean ones. Called by the scripts that compile the corpus."""
    found = []
    for path in files(CORPUS):
        hits = scan(path)
        found += hits
        stamp = json.load(open(stamp_of(path))) if os.path.exists(stamp_of(path)) else {}
        if hits:
            stamp.pop(os.path.basename(path), None)
        else:
            stamp[os.path.basename(path)] = sha256(path)
        json.dump(stamp, open(stamp_of(path), "w"), indent=1)
        print(f"  {os.path.relpath(path, HERE)}: {len(hits)} found", flush=True)
    return found


def main():
    found = [hit for path in files(FILES) for hit in scan(path)]
    if "--corpus" in sys.argv:
        found += scan_corpus()
    else:
        for path in files(CORPUS):
            stamp = json.load(open(stamp_of(path))) if os.path.exists(stamp_of(path)) else {}
            if stamp.get(os.path.basename(path)) != sha256(path):
                found.append(f"{os.path.relpath(path, HERE)}: changed or never scanned since it was compiled — run python tests/test_vegan.py --corpus")
    for f in found[:20]:
        print(" ", f)
    print(f"  {len(found)} animal products named, or corpus files unscanned, in rai's forms, scripts, training data, corpus and test sets")
    if found:
        sys.exit(1)


if __name__ == "__main__":
    main()
