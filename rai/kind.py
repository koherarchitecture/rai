"""Notion 2, the simple rule: an answer counts unless it is deferred, general, or empty. Plain patterns, no model.
0.3.7 (26 September 2026): probably, I think, whoever, someone, somebody, sometime, somewhere, anyone, anybody, wherever, whenever,
a while, all over the place and ages added; later no longer refuses a span of time (eleven days later); idk, dunno, no clue and pata nahi,
as people type them. 0.3.8 (28 September 2026): the same in Hinglish (shayad, yaad nahi, koi, kisi, kuch, sab, bahut, kabhi, kahin,
achha, theek, wahi and their spellings), and an answer that opens with normal; and Hindi evaluations (sasta, mehenga, badhiya, bekaar, theek-thaak, zabardast, mast), which judge a thing without naming anything, as nice and great do in English (28 Sep 2026); no honest answer in any test set or training row uses them. rai ka pahad's live rounds showed the reader passing five of six such answers, so this rule is what stops them;
no honest answer in any test set uses these words."""
import re

DEFERRED = re.compile(r"\b(not sure|no idea|don'?t know|dont know|to be decided|tbd|(?<!days )(?<!day )(?<!weeks )(?<!week )(?<!hours )(?<!hour )(?<!minutes )(?<!months )(?<!years )later|can'?t tell|cannot tell|ask me later|maybe|probably|i think|idk|dunno|no clue|pata nahi|pata nai|shayad|yaad nahi|yaad nai|maloom nahi|malum nahi|dekhna padega|baad mein)\b", re.I)
GENERAL = re.compile(r"\b(a lot of|lots of|many|everyone|everybody|various|all sorts|great|very useful|really useful|really nice|nice|fine|amazing|works well|the usual|whatever|things|stuff|something|hard to say|i guess|whoever|someone|somebody|sometime|somewhere|anyone|anybody|wherever|whenever|a while|all over the place|ages|koi|kisi|kuch|sab|sabhi|bahut|kaafi|kabhi|kahin|kahi|jab bhi|jahan bhi|jo bhi|achha|accha|acha|theek|thik|zyada|jyada|wahi|yahin|ajeeb|sasta|saste|sasti|mehenga|mehnga|mehngi|mehenge|mehange|badhiya|badiya|bekaar|bekar|theek-thaak|theek thaak|thik thak|zabardast|mast)\b|^normal\b", re.I)


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
