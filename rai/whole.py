"""A whole is a thing's questions; a notions set is the seven ways a description can be complete."""
import re
from fractions import Fraction
import yaml

# The seven notions of set 01. A description is complete when it passes all seven: seven parts, not a sum.
SEVEN = frozenset({"declared_parts", "answer_kind", "two_readers", "frame_roles", "conditions_closed", "no_dangling_names", "nothing_left_to_ask"})


def parse_md(text):
    """A whole written in Markdown: '# name', then a numbered list of questions, each optionally followed by an
    indented '- stem: ...' line. Any other line is a note for the person reading the file and is ignored."""
    w, q = {"questions": []}, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# ") and "notion" not in w:
            w["notion"] = s[2:].strip()
        elif re.match(r"^\d+[.)]\s+\S", s):
            q = {"id": f"q{len(w['questions']) + 1}", "text": re.sub(r"^\d+[.)]\s+", "", s)}
            w["questions"].append(q)
        elif q and re.match(r"^-?\s*stem:", s, re.I):
            q["stem"] = s.split(":", 1)[1].strip() + " "
    return w


def load_whole(path):
    text = open(path).read()
    w = parse_md(text) if path.endswith(".md") else yaml.safe_load(text)
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
