# rai training data — data card

**File.** `data/train-synth.jsonl`, 12,000 rows, one JSON object per line.

**Row.** `question`, `stem`, `answer`, `span` (the phrase in `answer` that answers `question`, or `null`) and `cls` (the class below).

```json
{"question": "Does it have any mark, crack, line or speck? Where?", "stem": "It has ", "answer": "A crack down one side.", "span": "a crack down one side", "cls": "bare"}
```

**How it was made.** Entirely from templates, by `scripts/synth.py` with `random.seed(7)` and 200 rows per question over the ten wholes in `wholes/`. No language model wrote any of it and no person's words are in it. Labels are known by construction: a row is answerable only when its answer is a phrase written for that question.

| class | rows | answer | label |
|---|---|---|---|
| bare | 4909 | a particular written for this question, said plainly | span |
| restating | 1227 | the question's stem read out, then the particular | span |
| evasive | 1752 | *The usual.*, *It works well.*, *Nothing special.* | none |
| deferred | 1201 | *To be decided.*, *I'd have to look.* | none |
| general | 1202 | *Hundreds of them.*, *All over the place.* | none |
| off-question | 1164 | a real answer to a different question of the same whole, of a different kind | none |
| empty | 545 | *-*, *ok*, an empty string | none |

**Held out.** Every phrase in `tests/testset-v1.jsonl` is removed from the templates before any row is written, including a phrase that would appear once a stem is read out before it. The script checks the finished rows again and stops if any repeats the test set.

**What it is like.** Short, plain answers about ordinary things, in English, with Indian particulars (rupee coins, a chai stall). Every honest answer is a checkable particular: a colour, a count, a comparison with a named thing, a place, a length of time.

**What it is not.** Not a sample of how people answer. It teaches the reader where an answer is in a sentence and when there is none; it says nothing about people.

**Regenerate.** `python scripts/synth.py 200` writes the same 12,000 rows.

**Licence.** CC-BY-4.0. Attribute Koher's rai.
