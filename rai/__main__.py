"""rai — tells whether a description is complete, and says only the word.

  python -m rai tally wholes/stone.yaml     a person marks each question and each notion by hand (0.1.0)
  python -m rai ask wholes/stone.yaml       the reader reads each typed answer; notions 1 and 2 decided in code (0.2.0)
"""
import sys, os
from .whole import load_whole, load_notions
from .tally import tally, word

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTIONS = os.path.join(HERE, "notions", "set-01.yaml")


def yes(prompt):
    return input(prompt + " [y/n] ").strip().lower().startswith("y")


def cmd_tally(path):
    whole = load_whole(path)
    notions = load_notions(NOTIONS)
    print(f"— {whole['notion']} —")
    answered = {q["id"]: yes(q["text"] + "  answered?") for q in whole["questions"]}
    passed = {n["id"]: yes(f"{n['id']}: {n['complete_when']}  passed?") for n in notions if n["id"] != "declared_parts"}
    print(word(tally(whole, answered, passed)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "tally":
        cmd_tally(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "ask":
        from .ask import ask
        from .reader import Reader
        t, _ = ask(sys.argv[2], Reader())
        print(word(t))   # notions 3-7 are not yet in code, so 0.2.0 can only ever say "not complete" honestly
    else:
        print(__doc__)
