# rai training data — data card

**File.** `data/train-synth.jsonl`, 23,200 rows over nineteen forms, one JSON object per line.

**Row.** `question`, `stem`, `answer`, `span` (the phrase in `answer` that answers `question`, or `null`) and `cls` (the class below).

```json
{"question": "Does it have any mark, crack, line or speck? Where?", "stem": "It has ", "answer": "A crack down one side.", "span": "a crack down one side", "cls": "bare"}
```

**How it was made.** From templates, by `scripts/synth.py` with `random.seed(7)` and 200 rows per question over the 116 questions of the nineteen forms in `wholes/`: ten everyday objects and moments, the record of an artwork (medium, size, maker, date, title, marks, where it is, where it was), and eight everyday events and things (a phone call, a repair, something lost and found, a ride, a message, a form filled in, a door, a phone's first screen). Labels are known by construction: a row is answerable only when its answer is a phrase written for that question.

**Who wrote the words.** From 0.3.6, every phrase that answers a question (`data/fill-comma.jsonl`, 908 phrases, 6 to 10 for most questions and fewer for four that Comma answered badly) and every evasive, deferred and general reply (`data/nonanswers-comma.jsonl`, 51) was written by [Comma v0.1-2T](https://huggingface.co/common-pile/comma-v0.1-2t) (Apache-2.0), a 7B base model from EleutherAI and collaborators trained on openly licensed text, the Common Pile v0.1 (Kandpal et al. 2025, [arXiv 2506.05209](https://arxiv.org/abs/2506.05209)); its makers note that licence laundering and wrong metadata mean they cannot guarantee every text it read was openly licensed. It ran locally. It was shown a question, its stem, the thing the form is about, and phrases of its own already kept, never phrases from any other source, and it wrote one more. Each output was read and judged before it was kept: it had to follow the stem, answer that question about that thing, name something plain and real, and not repeat a kept phrase. A little over half the phrases were kept, and one reply in three. The questions and stems were written for rai and not by Comma; the empty answers are marks and single words.

| class | rows | answer | label |
|---|---|---|---|
| bare | 9427 | a phrase written for this question, said plainly | span |
| restating | 2279 | the question's stem read out, then the phrase | span |
| evasive | 3510 | *It's a mystery.*, *That's a good question!*, *It was real nice.* | none |
| deferred | 2359 | *I will get back to you as soon as possible.*, *I am still figuring it out.* | none |
| general | 2254 | *Everyone, everywhere.*, *everything* | none |
| off-question | 2254 | a real answer to a different question of the same whole, of a different kind | none |
| empty | 1117 | *-*, *ok*, an empty string | none |

**Rows without a stem.** In every class except *restating*, whose answer already reads the stem out, three rows in ten carry an empty `stem`, so a missing stem is never itself a cue. Forms people write often have no stems.

**Held out.** Every phrase in every `tests/testset*.jsonl` is removed from the templates before any row is written, including a phrase that would appear once a stem is read out before it. The script checks the finished rows again and stops if any repeats a test set. It also stops if a training question repeats a question from `tests/unseen-forms/`, the four forms the reader is never trained on.

**What it is like.** Short, plain answers about ordinary things, in English, set in India (an auto driver's change, a ten-rupee coin, an Aadhaar photo, a bus stand). Comma's phrases are plainer and less local than hand-written ones would be, and some carry American words (*cellphone*, *neighbor*) that were kept when the phrase was otherwise sound. No answer names an animal product: tea is made with soy milk. Artwork makers are roles ("a lady", "no one knows"), never real artists, so no work is attributed to a real person. Every honest answer is a checkable particular: a colour, a count, a comparison with a named thing, a place, a length of time.

**What it is not.** Not a sample of how people answer. It teaches the reader where an answer is in a sentence and when there is none; it says nothing about people.

**Regenerate.** `python scripts/synth.py 200` writes the same 23,200 rows.

**Licence.** CC-BY-4.0. Attribute Koher's rai.
