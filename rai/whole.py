"""A whole is a thing's questions; a notions set is the seven ways a description can be complete."""
from fractions import Fraction
import yaml

# The seven notions of set 01. A description is complete when it passes all seven: seven parts, not a sum.
SEVEN = frozenset({"declared_parts", "answer_kind", "two_readers", "frame_roles", "conditions_closed", "no_dangling_names", "nothing_left_to_ask"})


def load_whole(path):
    w = yaml.safe_load(open(path))
    if not w or not w.get("questions"):
        raise SystemExit("no whole")
    n = len(w["questions"])
    for q in w["questions"]:
        q["weight"] = Fraction(1, n)   # weight comes only from position, never typed
    return w


def load_notions(path):
    s = yaml.safe_load(open(path))
    notions = s.get("notions") or []
    if len(notions) != 7:
        raise SystemExit(f"a notions set is exactly seven; this one has {len(notions)}")
    return notions
