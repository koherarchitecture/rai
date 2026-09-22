"""The tally. Complete or not complete, never why. Complete means all seven notions pass: seven parts, not a sum."""
from fractions import Fraction
from .whole import SEVEN


def declared_parts(whole, answered):
    """Notion 1: every question in the whole is answered. Returns the remainder of the whole."""
    return Fraction(1) - sum((q["weight"] for q in whole["questions"] if answered.get(q["id"])), Fraction(0))


def tally(whole, answered, passed):
    """answered: question id -> bool. passed: notion id -> bool for the other six notions.
    Returns the set of notions the description passes. Nothing is added up."""
    ok = {nid for nid, p in passed.items() if nid in SEVEN and nid != "declared_parts" and p}
    if declared_parts(whole, answered) == 0:
        ok.add("declared_parts")
    return ok


def word(passed):
    return "complete" if set(passed) == SEVEN else "not complete"
