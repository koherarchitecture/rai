# rai training data — data card

**Files.** `data/train-synth.jsonl`, the 29,000 rows 0.3.7 trains on: 0.3.6's 23,200 (`data/train-synth-0.3.6.jsonl`, described first below) and 5,800 new ones (`data/train-live.jsonl`, described under *0.3.7's rows*), shuffled together with seed 37. One JSON object per line.

**Row.** `question`, `stem`, `answer`, `span` (the phrase in `answer` that answers `question`, or `null`) and `cls` (the class below).

```json
{"question": "Does it have any mark, crack, line or speck? Where?", "stem": "It has ", "answer": "A crack down one side.", "span": "a crack down one side", "cls": "bare"}
```

**How it was made.** From templates, by `scripts/synth.py` with `random.seed(7)` and 200 rows per question over the 116 questions of the nineteen forms in `wholes/`: ten everyday objects and moments, the record of an artwork (medium, size, maker, date, title, marks, where it is, where it was), and eight everyday events and things (a phone call, a repair, something lost and found, a ride, a message, a form filled in, a door, a phone's first screen). Labels are known by construction: a row is answerable only when its answer is a phrase written for that question.

**Who wrote the words.** From 0.3.6, every phrase that answers a question (`data/fill-comma.jsonl`, 908 phrases, 6 to 10 for most questions and fewer for four that Comma answered badly) and every evasive, deferred and general reply (`data/nonanswers-comma.jsonl`, 51) was written by [Comma v0.1-2T](https://huggingface.co/common-pile/comma-v0.1-2t) (Apache-2.0), a 7B base model from EleutherAI and collaborators trained on openly licensed text, the Common Pile v0.1 (Kandpal et al. 2025, [arXiv 2506.05209](https://arxiv.org/abs/2506.05209)); its makers note that licence laundering and wrong metadata mean they cannot guarantee every text it read was openly licensed. It ran locally. It was shown a question, its stem, the thing the form is about, and phrases of its own already kept, never phrases from any other source, and it wrote one more. Each output was read and judged before it was kept: it had to follow the stem, answer that question about that thing, name something plain and real, and not repeat a kept phrase. A little over half the phrases were kept, and one reply in three. The questions and stems were written in Claude Code sessions, not by Comma, with a frontier model trained on other people's words; the empty answers are marks and single words.

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

## 0.3.7's rows

**How they were made.** By `scripts/synth_live.py 5800`, seed 37: a question built from a template and an ordinary thing (2,385 distinct questions, none of them rai's own, none about a thing in any test set), answered with the kind of thing the question asks for. The kinds: a person or a group or a role for *who*; a place, or an errand for where a person is; a time; a number or an ordinal; a colour; a material; a brand; a food; what a notice was about; what a verb takes (*what was being printed*); what makes a noise, a smell or a leak; a short reason; and Indian names, from a generator of about 230 first names and 50 family names across many languages and communities, alone, with a family name, an initial, or the honorific or kinship word people add (*bhai*, *di*, *garu*, *chettan*, *paaji*, *aapa*, *sir*, *ma'am*), drawn twice as often as any other kind. Half the honest answers are typed the way people type: lowercase, no question mark or full stop, sometimes wrapped in their own words (*like 20*, *X has it*). Non-answers are evasive, deferred, general or empty, or a real answer of a kind that does not answer (a page number for a *when*).

**Who wrote the words.** Every question, answer and name in these rows was written in Claude Code, on 26 and 27 September 2026, with a frontier model trained on other people's words. Nothing in them is Comma's.

**Held out.** Every answer in every test set, every question and thing in rai ka pahad's test set and the unseen forms, and the names and answers of the probes in `tests/probes/`. The vegan check passed before any reader was trained on them.

**Regenerate.** `python scripts/synth.py 200` writes 0.3.6's 23,200 rows to `data/train-synth-0.3.6.jsonl`; `python scripts/synth_live.py 5800` writes the new rows; `bash scripts/train-full.sh` shuffles them together and trains. Each step reproduces the shipped files byte for byte.

**Licence.** CC-BY-4.0. Attribute Koher's rai.
