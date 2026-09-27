"""The 0.3 contract: the calls, signatures and behaviour that programs built on rai rely on.
A change to rai that fails this test does not land. Run: python tests/test_contract.py"""
import inspect, json, os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole, load_notions, SEVEN
from rai.reader import Reader
from rai.ask import read_answers, READER, THRESHOLD
from rai.kind import counts
from rai.fit import fits
from rai.tally import word

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def test_current_reader_names_a_measured_pair():
    assert os.path.basename(READER).startswith("rai-") and THRESHOLD > 0
    assert inspect.signature(read_answers).parameters["threshold"].default == THRESHOLD


def test_the_current_reader_loads_and_reads():
    """The reader rai names as current, at the threshold rai names for it: a program built on rai uses exactly this pair."""
    present = [(READER, THRESHOLD)] if os.path.exists(os.path.join(READER, "config.json")) else []
    if not present:
        print("  (skipped: the current reader is not in runs/ — see the README)"); return
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


def test_rai_ka_pahad_round():
    # rai ka pahad's form (23 September 2026): a round's questions written live by a person, no stems, answers typed as people type them.
    # It must load through load_whole, read through read_answers, and at rai's threshold count no answer that does not answer.
    import tempfile
    md = "# Does the corridor bulb flicker more at night?\n\n1. who changed it last\n2. When did it start?\n3. how many times did it go off\n"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(md)
    whole = load_whole(f.name)
    assert [q.get("stem", "") for q in whole["questions"]] == ["", "", ""]
    reader = Reader(READER)
    found = read_answers(whole, {q["id"]: "idk" for q in whole["questions"]}, reader, THRESHOLD)
    assert not any(found.values())
    for name in ("testset-kapahad-v1.jsonl", "testset-typing-v1.jsonl", "testset-typing-v2.jsonl"):
        for r in map(json.loads, open(os.path.join(HERE, "tests", name))):
            if r["label"]:
                continue
            span, margin = reader.read(r["question"], r["answer"], "")
            assert not (span is not None and margin > THRESHOLD and counts(r["answer"]) and fits(r["question"], span)), (name, r["question"], r["answer"], margin)
