# How rai works

rai turns a set of typed answers into one of two answers, *complete* or *not complete*. Four parts do the work, and only the first uses a model.

## 1. The whole

A whole is a YAML file in `wholes/`: the questions that make up a complete description of one thing, written before anyone answers.

```yaml
notion: a stone
kind_rule: simple
questions:
  - id: colour
    text: "What colour is it?"
    stem: "It is "
    kind: fact
    counts_when: "a named colour, or two"
```

`rai/whole.py` loads it and gives each question an equal share of 1 by position. With six questions each is worth exactly 1/6. Nobody types a weight, so nobody can make one question matter more than another.

## 2. The reader

`rai/reader.py` holds the only model in rai: an extractive question-answering model with 33 million parameters. For each question it reads the typed answer and does one of two things:

- points at the phrase in the answer that answers the question, or
- says there is no answer.

It reads the question's stem and the answer together (*It is* + *dark grey*), because a bare answer like *dark grey* is easier to place after its stem. The stem is only a reading aid.

It returns the phrase and a **margin**: the score of its best phrase minus the score of *no answer*. Two guards follow:

- **The verbatim guard.** The phrase must appear, word for word, in what the person typed. A phrase found only in the stem does not count. The model has no way to add a word.
- **The threshold.** The margin must be above a fixed number, set in `rai/ask.py`. The number is chosen as the smallest margin that lets no non-answer in the test set through, rounded up, never down. `tests/test_reader_v03.py` fails if the number in `rai/ask.py` would let one through.

## 3. The kind rule

`rai/kind.py` sorts each answer with plain patterns, no model:

| kind | examples | counts? |
|---|---|---|
| particular | *dark grey*, *six minutes*, *the path outside the library* | yes |
| deferred | *not sure*, *later*, *to be decided* | no |
| general | *lots of things*, *the usual*, *really nice* | no |
| empty | nothing, *-*, *?* | no |

An answer with a number in it is never called general.

## 4. The tally

`rai/tally.py` checks which of the seven notions a description passes.

- **Notion 1, declared parts**, passes when every question has been answered: every question found by the reader, above the threshold, and of a kind that counts. Inside a whole, each question is an equal share of 1, kept as an exact fraction so that a whole with nested questions still comes to exactly nothing left over when every question is answered.
- **Notion 2, answer kind**, passes when every answer is a particular. The notion also admits an owned position for a *why*; the simple rule in this release does not yet recognise one.
- **Notions 3 to 7** are, in this release, marked by a person as yes or no, until the versions that put them in code arrive.

**Complete means all seven pass.** The seven are parts, not a sum: nothing is added up, and there is no value between *not complete* and *complete*. The function `word()` returns *complete* only when the set of notions passed is exactly the seven, and nothing else leaves the tally.

## Why the reader never decides

A model asked whether a description is complete would answer, and its answer would sound like a judgement. rai never asks it that. The model is asked something much smaller: where in this sentence is the answer to this question? What counts, and what complete means, is written in code and in `notions/set-01.yaml`, where anyone can read it, disagree with it, and change it in their own copy.

This is the split [Split-Domain Cognition](https://splitdomaincognition.org) describes: language work and judgement work are different kinds of work, and failures follow when one channel does both.

## What is never shown

The margin, the fraction, the notions passed and the phrase the reader found are all internal. The person sees only *complete* or *not complete*. rai gives no reason for *not complete*, because a reason would point to the fix.
