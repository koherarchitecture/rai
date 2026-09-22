"""Notion 2, the simple rule: an answer counts unless it is deferred, general, or empty. Plain patterns, no model."""
import re

DEFERRED = re.compile(r"\b(not sure|no idea|don'?t know|dont know|to be decided|tbd|later|can'?t tell|cannot tell|ask me later|maybe)\b", re.I)
GENERAL = re.compile(r"\b(a lot of|lots of|many|everyone|everybody|various|all sorts|great|very useful|really useful|really nice|nice|fine|amazing|works well|the usual|whatever|things|stuff|something|hard to say|i guess)\b", re.I)


def kind(answer):
    a = answer.strip()
    if len(a.split()) < 1 or a in {"-", "—", "?"}:
        return "empty"
    if DEFERRED.search(a):
        return "deferred"
    if GENERAL.search(a) and not re.search(r"\d", a):
        return "general"
    return "particular"


def counts(answer):
    return kind(answer) == "particular"
