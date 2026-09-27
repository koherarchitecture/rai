"""Notion 2, the simple rule: an answer counts unless it is deferred, general, or empty. Plain patterns, no model.
0.3.7 (26 September 2026): probably, I think, whoever, someone, somebody, sometime, somewhere, anyone, anybody, wherever, whenever,
a while, all over the place and ages added; later no longer refuses a span of time (eleven days later); idk, dunno, no clue and pata nahi,
as people type them. rai ka pahad's live rounds showed the reader passing five of six such answers, so this rule is what stops them;
no honest answer in any test set uses these words."""
import re

DEFERRED = re.compile(r"\b(not sure|no idea|don'?t know|dont know|to be decided|tbd|(?<!days )(?<!day )(?<!weeks )(?<!week )(?<!hours )(?<!hour )(?<!minutes )(?<!months )(?<!years )later|can'?t tell|cannot tell|ask me later|maybe|probably|i think|idk|dunno|no clue|pata nahi|pata nai)\b", re.I)
GENERAL = re.compile(r"\b(a lot of|lots of|many|everyone|everybody|various|all sorts|great|very useful|really useful|really nice|nice|fine|amazing|works well|the usual|whatever|things|stuff|something|hard to say|i guess|whoever|someone|somebody|sometime|somewhere|anyone|anybody|wherever|whenever|a while|all over the place|ages)\b", re.I)


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
