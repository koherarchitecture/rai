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

# rai reader 0.3.4 — model card

**What it is.** An extractive question-answering model. Given a question and a short typed answer, it returns the phrase in the answer that answers the question, or nothing. It cannot generate text. It is the reading part of [rai](https://github.com/koherarchitecture/rai), a tool that says only whether a description is complete under a notion of completeness written down in advance. Every decision after the reading is made in plain code.

**Trained from.** [deepset/minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2) (CC-BY-4.0), deepset's fine-tune of Microsoft's [MiniLM-L12-H384-uncased](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) (MIT) on SQuAD 2.0. Same architecture, 33M parameters, nothing added. Credit to deepset and Microsoft.

**Trained on.** 13,600 synthetic pairs over eleven forms, labels known by construction, made from templates by `scripts/synth.py` (seed 7): honest answers given bare or after the question's stem, and evasive, deferred, general, empty and off-question answers labelled *no answer*. No person's words. Ten forms describe everyday objects and moments; the eleventh is the record of an artwork. Two epochs, batch 32, learning rate 2e-5, maximum length 384, on CPU, about eight minutes. See `DATA-CARD.md`.

**Measured** on two test sets it never saw, at one threshold — **14.89**, the smallest margin that lets no non-answer through in either. On **test set v1** (360 rows over the ten everyday forms) it counts **146 of 180** honest answers and no non-answer. On the **artwork set** (48 rows) it counts **20 of 24** and no non-answer. The untrained deepset model, given the same stems, counts 16 of 180 on test set v1. No phrase in either test set appears in the training data.

**Scope.** The reader is for forms: a short list of questions written in advance, each asking for a concrete particular (a name, a number, a place, a time, a colour, a comparison with a named thing), answered in short typed phrases. It is not a general completeness checker and does not judge whether an answer is right or enough. It was trained on eleven forms: ten about everyday objects and moments, and the record of an artwork. On forms it was not trained on it refuses evasive answers as before but misses more real ones: in single tries on 22 September 2026, 4 of 6 on an unseen object form and 1 of 3 on a handover-note form. See the README's *Scope* section.

**Limits.**
- The threshold is chosen on the same test set it is reported on.
- The test sets and the training data are built from the same kind of template: short, plain, particular answers over the same eleven forms. They share no phrase, but they share a style. Performance on answers people type in their own words is not measured.
- The artwork set has 24 real answers. It shows the reader can read an artwork record; it does not say how well, to any precision.
- One training run, one seed.
- English only. Answers mentioning Indian coins, places and brands appear throughout, because the templates were written in India.

**How to use it.**

```python
from rai.reader import Reader
r = Reader("prayasabhinav/rai")        # or a local folder
span, margin = r.read("What colour is it?", "Dark grey, with a rusty patch.", stem="It is ")
counted = span is not None and margin > 14.89
```

With plain transformers it behaves as any SQuAD 2.0 extractive model, but the threshold above only holds with rai's reading rule in `rai/reader.py`: the best span against the null answer, a span no longer than 30 tokens, and the span required to appear verbatim in the typed answer.

**Out of scope.** It does not grade, suggest or give reasons, and its margin is not shown to anyone. It is not for use as a step in a decision that affects somebody else.

**Licence.** CC-BY-4.0. Attribute Koher's rai reader, and deepset and Microsoft as above.
