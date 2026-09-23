# rai training data — data card

**File.** `data/train-synth.jsonl`, 23,200 rows over nineteen forms, one JSON object per line.

**Row.** `question`, `stem`, `answer`, `span` (the phrase in `answer` that answers `question`, or `null`) and `cls` (the class below).

```json
{"question": "Does it have any mark, crack, line or speck? Where?", "stem": "It has ", "answer": "A crack down one side.", "span": "a crack down one side", "cls": "bare"}
```

**How it was made.** Entirely from templates, by `scripts/synth.py` with `random.seed(7)` and 200 rows per question over the 116 questions of the nineteen forms in `wholes/`: ten everyday objects and moments, the record of an artwork (medium, size, maker, date, title, marks, where it is, where it was), and eight everyday events and things added in 0.3.5 (a phone call, a repair, something lost and found, a ride, a message, a form filled in, a door, a phone's first screen). No language model wrote any of it and no person's words are in it. Labels are known by construction: a row is answerable only when its answer is a phrase written for that question.

| class | rows | answer | label |
|---|---|---|---|
| bare | 9435 | a particular written for this question, said plainly | span |
| restating | 2283 | the question's stem read out, then the particular | span |
| evasive | 3487 | *The usual.*, *It works well.*, *Nothing special.* | none |
| deferred | 2318 | *To be decided.*, *I'd have to look.* | none |
| general | 2283 | *Hundreds of them.*, *All over the place.* | none |
| off-question | 2291 | a real answer to a different question of the same whole, of a different kind | none |
| empty | 1103 | *-*, *ok*, an empty string | none |

**Rows without a stem.** In every class except *restating*, whose answer already reads the stem out, three rows in ten carry an empty `stem`, so a missing stem is never itself a cue. Forms people write often have no stems.

**Held out.** Every phrase in every `tests/testset*.jsonl` is removed from the templates before any row is written, including a phrase that would appear once a stem is read out before it. The script checks the finished rows again and stops if any repeats a test set. It also stops if a training question repeats a question from `tests/unseen-forms/`, the four forms the reader is never trained on.

**What it is like.** Short, plain answers about ordinary things, in English, with Indian particulars (rupee coins, a chai stall, an auto ride). No answer names an animal product: tea is made with soy milk. The artwork rows name materials, sizes, dates, titles, marks and places; makers are roles and workshops ("my grandmother", "a potter in Khurja", "unknown"), never real artists, so no work is attributed to a real person. Every honest answer is a checkable particular: a colour, a count, a comparison with a named thing, a place, a length of time.

**What it is not.** Not a sample of how people answer. It teaches the reader where an answer is in a sentence and when there is none; it says nothing about people.

**Regenerate.** `python scripts/synth.py 200` writes the same 23,200 rows.

**Licence.** CC-BY-4.0. Attribute Koher's rai.
