"""The 0.3 contract: the calls, signatures and behaviour that programs built on rai rely on.
A change to rai that fails this test does not land. Run: python tests/test_contract.py"""
import inspect, os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole, load_notions, SEVEN
from rai.reader import Reader
from rai.ask import read_answers
from rai.kind import counts
from rai.tally import word

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# whichever 0.3 reader is present, with the threshold it was measured at
READERS = [(os.path.join(HERE, "runs", "rai-0.3-full"), 14.56), (os.path.join(HERE, "runs", "rai-0.3.4"), 14.89)]


def test_load_whole_yaml_and_md():
    for name in ("stone.yaml", "key.md"):
        w = load_whole(os.path.join(HERE, "wholes", name))
        assert w["notion"] and w["questions"]
        n = len(w["questions"])
        for q in w["questions"]:
            assert q["id"] and q["text"] and q["weight"] == Fraction(1, n)


def test_read_answers_signature():
    assert list(inspect.signature(read_answers).parameters)[:4] == ["whole", "answers", "reader", "threshold"]


def test_counts():
    for a in ("Not sure yet.", "Lots of things.", "", "-"):
        assert counts(a) is False, a
    for a in ("Dark grey with a rusty patch.", "About ten minutes.", "The path behind the post office."):
        assert counts(a) is True, a


def test_word_is_all_seven():
    assert {n["id"] for n in load_notions(os.path.join(HERE, "notions", "set-01.yaml"))} == SEVEN
    assert word(set(SEVEN)) == "complete"
    for missing in SEVEN:
        assert word(set(SEVEN) - {missing}) == "not complete"
    assert word(set()) == "not complete"


def test_the_03_readers_load_and_read():
    present = [(p, t) for p, t in READERS if os.path.exists(os.path.join(p, "config.json"))]
    if not present:
        print("  (skipped: no reader in runs/ — see the README)"); return
    w = load_whole(os.path.join(HERE, "wholes", "stone.yaml"))
    real = {q["id"]: a for q, a in zip(w["questions"], ["Dark grey with a rusty patch.", "About the size of my thumbnail.", "A wedge.", "Rough and cold.", "A white speck near one end.", "The path behind the post office."])}
    evasive = {q["id"]: "Not sure yet." for q in w["questions"]}
    for path, threshold in present:
        r = Reader(path)
        found = read_answers(w, real, r, threshold)
        assert set(found) == {q["id"] for q in w["questions"]} and all(isinstance(v, bool) for v in found.values()), path
        assert all(found.values()), (path, found)
        assert not any(read_answers(w, evasive, r, threshold).values()), path


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
