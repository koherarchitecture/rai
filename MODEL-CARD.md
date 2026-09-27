---
license: cc-by-4.0
language:
- en
library_name: transformers
pipeline_tag: question-answering
base_model: deepset/minilm-uncased-squad2
tags:
- extractive-question-answering
- completeness
- split-domain-cognition
- synthetic-data
- cpu
---

# rai reader 0.3.7 — model card

**What it is.** An extractive question-answering model. Given a question and a short typed answer, it returns the phrase in the answer that answers the question, or nothing. It cannot generate text. It is the reading part of [rai](https://github.com/koherarchitecture/rai), a tool that says only whether a description is complete under a notion of completeness written down in advance. Every decision after the reading is made in plain code.

**Trained from.** [deepset/minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2) (CC-BY-4.0), deepset's fine-tune of Microsoft's [MiniLM-L12-H384-uncased](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) (MIT) on SQuAD 2.0. Same architecture, 33M parameters, nothing added. Credit to deepset and Microsoft.

**0.3.7 trains on 0.3.6's rows and 5,800 more written in Claude Code.** In 0.3.6's rows the answers were written by Comma v0.1, a model trained only on openly licensed and public-domain text, and the questions and stems in Claude Code sessions. The new rows, questions and answers both, were written in Claude Code, with a frontier model trained on other people's words. The reader it is trained from, deepset's MiniLM fine-tuned on SQuAD 2.0, was not built from openly licensed text.

**Trained on.** 29,000 synthetic pairs, labels known by construction. 23,200 are 0.3.6's, over nineteen forms, made by `scripts/synth.py` (seed 7): honest answers given bare or after the question's stem, and evasive, deferred, general, empty and off-question answers labelled *no answer*, three rows in ten without their stem. 5,800 are new, made by `scripts/synth_live.py` (seed 37): questions as people write them, with no stem, answered with the kind of thing each asks for (a person, a place or an errand, a time, a number, a brand, a food, what a verb takes, what makes a noise, an Indian name), half typed the way people type, with wrong-kind answers labelled *no answer*. No person's answers are in it, and no animal product is named, by Koher's rule for every model it trains. Two epochs, batch 32, learning rate 2e-5, maximum length 384, about 3 minutes a seed on a Mac's GPU. The recipe was run with seeds 7, 1 and 2 and the three readers' weights averaged into this one (a uniform model soup, Wortsman et al. 2022). See `DATA-CARD.md`.

**Measured** on six test sets it never trained on, at one threshold, **8.92**, the smallest margin that lets no non-answer through in any of them, with rai's two kind rules applied (`rai/kind.py`, `rai/fit.py`): **157 of 180** on test set v1, **20 of 24** on the artwork set, **66 of 96** on the unseen forms (33 of 48 with the form's stem, 33 without), **52 of 60** on rai ka pahad rounds, and **21 of 24** and **44 of 46** on two sets of people's typing. It counts no non-answer in any set. 0.3.6, scored the same way, counted 161, 20, 62, 42, 4 and 1. On three probes written before the last training and never trained on: 20 of 20 in a batch of people's typing, 120 of 123 Indian names that no training row contains, and 17 of 20 answers that mean the right thing in free wording, with one non-answer counted (*the peon* for what was being photocopied). No phrase in any test set appears in the training data.

**Scope.** The reader is for forms: a short list of questions written in advance, each asking for a concrete particular (a name, a number, a place, a time, a colour, a comparison with a named thing), answered in short typed phrases. It is not a general completeness checker and does not judge whether an answer is right or enough. It was trained on nineteen forms: eighteen about everyday objects, moments and events, and the record of an artwork. On forms it was not trained on it refuses non-answers as before but misses more real ones, 66 of 96 on the unseen set against 157 of 180 on test set v1. See the README's *Scope* section.

**Limits.**
- The threshold is chosen on the same test set it is reported on.
- Every test answer was written in Claude Code, including the people's-typing sets, which stand in for people. They share no phrase with the training data. Performance on rounds written by people who use rai is not measured.
- It still counts one kind of wrong answer in the probes: a person given for a *what* (*the peon* for what was being photocopied).
- The smaller sets have 24 to 96 real answers. A change of one or two answers between versions says nothing on its own.
- Three pointings, averaged. One pointing alone moves the count by about thirty.
- *Nothing special.* counts as an answer to *Does it have any mark?* (margin 14.2), read as *no marks worth naming*; 0.3.5 refused it. On the other questions tried it is refused as before.
- English only, with Indian names, words (*ji*, *di*, *garu*, *chettan*) and places throughout, because the templates were written in India, in Claude Code sessions.

**How to use it.**

```python
from rai.reader import Reader
r = Reader("prayasabhinav/rai")        # or a local folder
span, margin = r.read("What colour is it?", "Dark grey, with a rusty patch.", stem="It is ")
counted = span is not None and margin > 8.92   # rai also applies rai/kind.py and rai/fit.py
```

With plain transformers it behaves as any SQuAD 2.0 extractive model, but the threshold above only holds with rai's reading rule in `rai/reader.py`: the best span against the null answer, a span no longer than 30 tokens, and the span required to appear verbatim in the typed answer; and rai's two kind rules, `rai/kind.py` and `rai/fit.py`, which the threshold was measured with.

**Out of scope.** It does not grade, suggest or give reasons, and its margin is not shown to anyone. It is not for use as a step in a decision that affects somebody else.

**Licence.** CC-BY-4.0. Attribute Koher's rai reader, and deepset and Microsoft as above.
