# What rai can be used for

rai answers one narrow question: given a set of questions written in advance and a set of typed answers, is every part there? The uses below are the ones that fit inside that. Each works with this release.

## 1. Checking your own description before you share it

Write a whole for the kind of thing you describe often: what a description of it has to contain, as questions that can each be answered with a particular. Then answer your own questions and let rai tally.

*Example.* Someone who writes the same kind of handover note every week writes `wholes/handover.yaml` with six questions: what was finished, what is half-done and where it stands, what is blocked and on whom, where the files are, what happens next and by when, who to ask. Before sending the note, they type their answers and run it. *Not complete* sends them back to their own note, with no hint about which part.

This is for your own use, on your own machine. rai's output is meant for the person who wrote the answers, and for nobody else.

## 2. A pastime for two, built on top of it

rai was made for small, harmless descriptions: a stone, the last cup of tea, a queue. Two people at one keyboard, one asking and typing, the other answering; one word at the end; *not complete* means they talk and answer again. The ten wholes in `wholes/` are written for this use.

rai itself is only the model and the tally. A pastime like this is a separate program that calls it:

```python
found = read_answers(whole, answers, reader)
```

and keeps its own interface. Koher is building one such pastime separately.

## 3. The reader on its own: does this text answer this question, and where?

The reader can be used without the tally. Given a question and a short piece of text, it returns the exact phrase that answers the question, or nothing, and a margin. It cannot invent a phrase: the answer must appear word for word in the text.

*Example.* A person keeps short daily notes and wants to know, for their own notes, which ones say *where* something happened. They ask the reader "Where did it happen?" of each note and keep the ones where it points at a phrase above the threshold.

The threshold of 14.56 was set on short, plain answers about ordinary things. On longer or different text it is a starting point and needs checking.

## 4. Writing your own wholes

A whole is a YAML file, so a whole for anything you describe can be written in a few minutes. The rules that keep a whole checkable are in [`wholes.md`](wholes.md): one thing per question, every question answerable with a particular, no leading questions, plain words. Comparisons make vague things checkable (*how big, against a coin?*).

Nothing in rai limits wholes to ten. `rai/whole.py` loads any file in the format.

## 5. A small benchmark for extractive readers

`tests/testset-v1.jsonl` (360 rows) and `data/train-synth.jsonl` (12,000 rows) are a public, labelled set of short typed answers. The test set has honest, evasive and off-question answers; the training data also has deferred, general, restating and empty ones. Any extractive question-answering model can be scored on them with `scripts/eval_reader.py`, which reports false presents, false absents and honest answers counted at the threshold that lets no non-answer through. The test set shares no phrase with the training data.

## 6. A worked example of keeping a model out of a decision

rai's code, with its scripts, is about 530 lines. It shows one way of using a language model where the model is asked only a small, checkable question (where is the answer in this sentence?), and everything that decides is written in plain code and a YAML file anyone can read and change. It can be read, forked and adapted as a reference for that arrangement, which [Split-Domain Cognition](https://splitdomaincognition.org) describes in general.

## What rai must not be used for

- **Checking somebody else's work inside a procedure**: a form someone must fill in, an application, an assessment, a report someone is required to file. rai's *not complete* is a prompt for the person who wrote the answers. Put inside a procedure, it becomes a gate, and rai is built to keep a model out of gates.
- **Grading or scoring anything.** There is no score to extract; the tally is never shown and the fraction means nothing outside the notion of completeness it was written for.
- **Judging whether anything is good, true or safe.** rai checks that a part is present, never what the part says.
- **Telling anybody what is missing.** rai will not, by design. A tool that adds this back no longer follows rai's design.
- **Keeping what people type.** Nothing in rai stores answers. A program built on it should not either.
