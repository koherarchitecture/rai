# What rai can be used for

rai answers one narrow question: given a set of questions written in advance and a set of typed answers, is every part there? The uses below are the ones that fit inside that. Each works with this release.

## 1. Checking a description against its form

Write the form once: the questions a complete description of one kind of thing or event has to answer. Then answer them and let rai tally. The form stays within [rai's scope](../README.md#scope-the-kind-of-set-rai-is-for): every question answered by a short particular.

*Example.* Someone returning a camera kit to a studio store writes `wholes/equipment-return.md`: what is being returned, what condition it is in and where any damage is, whether anything is missing, when it was taken out and when it is being returned, where it is now. Before handing the kit back, they type their answers and run it. *Not complete* sends them back to their own answers, with no hint about which part.

This is for your own use, on your own machine. rai's output is meant for the person who wrote the answers, and for nobody else. On a set it was not trained on, rai misses more real answers than on the sets it was trained on (59 of 96 on four unseen forms, against 155 of 180 on the first ten), so *not complete* there is more often rai's miss than a missing part.

## 2. Writing your own wholes

A set is a short Markdown file (or YAML, like the nineteen shipped), so a set for one ordinary thing can be written in a few minutes; the format is in the README's [How to use](../README.md#how-to-use). The rules that keep a whole checkable are in [`wholes.md`](wholes.md): one thing per question, every question answerable with a particular, no leading questions, plain words. Comparisons make vague things checkable (*how big, against a coin?*).

Nothing in rai limits which sets it runs. `rai/whole.py` loads any `.md` or `.yaml` file in the format. What limits them is the reader's training: it knows the nineteen shipped sets well, sets like them partly, and other kinds of description poorly.

## 3. A small benchmark for extractive readers

`tests/testset-v1.jsonl` (360 rows), `tests/testset-artwork-v1.jsonl` (48), `tests/testset-unseen-v1.jsonl` (168, over four forms the reader never trains on) and `data/train-synth.jsonl` (23,200 rows) are a public, labelled set of short typed answers. The test set has honest, evasive and off-question answers; the training data also has deferred, general, restating and empty ones. Any extractive question-answering model can be scored on them with `scripts/eval_reader.py`, which reports false presents, false absents and honest answers counted at the threshold that lets no non-answer through. The test sets share no phrase with the training data.

## 4. A worked example of keeping a model out of a decision

rai's code, with its scripts, is about 530 lines. It shows one way of using a language model where the model is asked only a small, checkable question (where is the answer in this sentence?), and everything that decides is written in plain code and a YAML file anyone can read and change. It can be read, forked and adapted as a reference for that arrangement, which [Split-Domain Cognition](https://splitdomaincognition.org) describes in general.

## What rai must not be used for

- **Checking somebody else's work inside a procedure**: a form someone must fill in, an application, an assessment, a report someone is required to file. rai's *not complete* is a prompt for the person who wrote the answers. Put inside a procedure, it becomes a gate, and rai is built to keep a model out of gates.
- **Grading or scoring anything.** There is no score to extract; the tally is never shown and the fraction means nothing outside the notion of completeness it was written for.
- **Judging whether anything is good, true or safe.** rai checks that a part is present, never what the part says.
- **Telling anybody what is missing.** rai will not, by design. A tool that adds this back no longer follows rai's design.
- **Keeping what people type.** Nothing in rai stores answers. A program built on it should not either.
