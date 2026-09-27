"""0.3.7: whether the phrase the reader found is the kind of thing the question asks for, where plain patterns can tell. No model.
A bare number or ordinal (7th, 200, the 2nd) answers only a question that asks for a number, a position or a time; a label (Page 17,
Room 204, Bus 51) never answers a who, a when or a why. The reader cannot tell these apart well, and before this rule the threshold had
to sit above them, refusing correct answers just below it (26 September 2026: 7th for where a key was left, Page 17 for when)."""
import re

NUMBER = re.compile(r"^(the |like |around |about )?(\d[\d,.:]*|\d+(st|nd|rd|th)|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)$", re.I)
LABEL = re.compile(r"^(the )?(page|room|row|bus|platform|locker|chapter|no\.?|number|seat|gate|window) ?no\.? ?\d+$|^(page|room|row|bus|platform|locker|chapter|seat|number) \d+$", re.I)
ASKS_NUMBER = re.compile(r"\b(how many|how much|how far|how old|how long|how big|how heavy|how often|which|what number|what time|what speed|what size|what year|what date|when|whose turn)\b", re.I)
NOT_A_LABEL = re.compile(r"^\s*(who|when|why)\b|\bwhat time\b|\bhow (many|much|long)\b", re.I)


def fits(question, span):
    s = span.strip().rstrip(".")
    if NUMBER.match(s):
        return bool(ASKS_NUMBER.search(question))
    if LABEL.match(s):
        return not NOT_A_LABEL.search(question)
    return True
