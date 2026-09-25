"""0.2.0: asks a whole's questions, reads each typed answer, decides notions 1 and 2 in code. Complete or not complete, never why."""
from .whole import load_whole
from .kind import counts
from .reader import Reader
import os

# The current reader and the threshold measured for it. They move together, at every release, and nowhere else:
# a program built on rai uses these two and gets the latest reader that passed the contract (tests/test_contract.py).
READER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs", "rai-0.3.6")
THRESHOLD = 9.30   # margin the reader must clear; set at zero false presents over test set v1, the artwork set and the unseen set together, for runs/rai-0.3.6 (scripts/eval_reader.py)


def read_answers(whole, answers, reader, threshold=THRESHOLD):
    """answers: question id -> typed text. Returns question id -> bool (found, above threshold, and of a kind that counts)."""
    found = {}
    for q in whole["questions"]:
        a = answers.get(q["id"], "")
        span, margin = reader.read(q["text"], a, q.get("stem", "")) if a.strip() else (None, 0)
        found[q["id"]] = span is not None and margin > threshold and counts(a)
    return found


def notions_in_code(found, kinds_ok):
    """Notions 1 and 2 are decided here; the other five are marked by people until their versions ship."""
    return ({"declared_parts"} if all(found.values()) else set()) | ({"answer_kind"} if kinds_ok else set())


def ask(path, reader):
    whole = load_whole(path)
    print(f"— {whole['notion']} —")
    answers = {q["id"]: input(q["text"] + " ") for q in whole["questions"]}
    found = read_answers(whole, answers, reader)
    kinds_ok = all(counts(a) for a in answers.values())
    return notions_in_code(found, kinds_ok), answers
