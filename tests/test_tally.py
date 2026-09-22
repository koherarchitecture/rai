"""Hand-worked cases for the tally. Run: python -m pytest tests -q, or python tests/test_tally.py"""
import os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole, load_notions, SEVEN
from rai.tally import declared_parts, tally, word

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STONE = os.path.join(HERE, "wholes", "stone.yaml")
NOTIONS = os.path.join(HERE, "notions", "set-01.yaml")
OTHER_SIX = ["answer_kind", "two_readers", "frame_roles", "conditions_closed", "no_dangling_names", "nothing_left_to_ask"]


def marks(whole, *missing):
    return {q["id"]: q["id"] not in missing for q in whole["questions"]}


def test_all_answered_all_passed_is_complete():
    w = load_whole(STONE)
    assert word(tally(w, marks(w), {n: True for n in OTHER_SIX})) == "complete"


def test_one_question_missing_is_not_complete():
    w = load_whole(STONE)
    assert declared_parts(w, marks(w, "marks")) == Fraction(1, 6)
    assert word(tally(w, marks(w, "marks"), {n: True for n in OTHER_SIX})) == "not complete"


def test_six_of_seven_is_not_complete():
    w = load_whole(STONE)
    passed = {n: True for n in OTHER_SIX}; passed["two_readers"] = False
    assert word(tally(w, marks(w), passed)) == "not complete"


def test_order_does_not_matter():
    w = load_whole(STONE)
    a = {n: n in ("answer_kind", "frame_roles") for n in OTHER_SIX}
    b = {n: n in ("frame_roles", "answer_kind") for n in reversed(OTHER_SIX)}
    assert tally(w, marks(w), a) == tally(w, marks(w), b)


def test_the_seven_are_set_01():
    assert {n["id"] for n in load_notions(NOTIONS)} == SEVEN


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
