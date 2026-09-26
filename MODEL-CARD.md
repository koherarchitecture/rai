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

# rai reader 0.3.6 — model card

**What it is.** An extractive question-answering model. Given a question and a short typed answer, it returns the phrase in the answer that answers the question, or nothing. It cannot generate text. It is the reading part of [rai](https://github.com/koherarchitecture/rai), a tool that says only whether a description is complete under a notion of completeness written down in advance. Every decision after the reading is made in plain code.

**Trained from.** [deepset/minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2) (CC-BY-4.0), deepset's fine-tune of Microsoft's [MiniLM-L12-H384-uncased](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) (MIT) on SQuAD 2.0. Same architecture, 33M parameters, nothing added. Credit to deepset and Microsoft.

**The answers 0.3.6 trains on were written by Comma v0.1**, a model trained only on openly licensed and public-domain text. The questions and stems were written in Claude Code sessions, not by Comma, with a frontier model trained on other people's words, and the reader it is trained from, deepset's MiniLM fine-tuned on SQuAD 2.0, was not built from openly licensed text.

**Trained on.** 23,200 synthetic pairs over nineteen forms, labels known by construction, made from templates by `scripts/synth.py` (seed 7): honest answers given bare or after the question's stem, and evasive, deferred, general, empty and off-question answers labelled *no answer*. Three rows in ten reach the reader without their stem, honest answers and non-answers alike. The words in the answers were written by [Comma v0.1-2T](https://huggingface.co/common-pile/comma-v0.1-2t), a model trained on openly licensed text, and each was judged before it was kept; no person's answers are in it, and no animal product is named. Eighteen forms describe everyday objects, moments and events; one is the record of an artwork. Two epochs, batch 32, learning rate 2e-5, maximum length 384, on CPU, about 28 minutes a seed on 4 ARM cores. The recipe was run with seeds 7, 1 and 2 and the three readers' weights averaged into this one (a uniform model soup, Wortsman et al. 2022). See `DATA-CARD.md`.

**Measured** on three test sets it never saw, at one threshold, **9.30**, the smallest margin that lets no non-answer through in any of them. On **test set v1** (360 rows over the first ten everyday forms) it counts **161 of 180** honest answers. On the **artwork set** (48 rows) it counts **20 of 24**. On the **unseen set** (168 rows over four forms it was never trained on) it counts **61 of 96**: 31 of 48 read with the form's stem and 30 of 48 without. It counts no non-answer in any set. The three seeds alone counted 223, 226 and 221 of 300 in all; their average counts 242. The previous reader, 0.3.5, whose answers were not written by Comma, counted 155, 21 and 59 at 12.67. A threshold belongs to the reader it was measured for, so 9.30 and 12.67 are not comparable as numbers. No phrase in any test set appears in the training data, and no training question repeats a question from an unseen form.

**Scope.** The reader is for forms: a short list of questions written in advance, each asking for a concrete particular (a name, a number, a place, a time, a colour, a comparison with a named thing), answered in short typed phrases. It is not a general completeness checker and does not judge whether an answer is right or enough. It was trained on nineteen forms: eighteen about everyday objects, moments and events, and the record of an artwork. On forms it was not trained on it refuses non-answers as before but misses more real ones, 61 of 96 on the unseen set against 161 of 180 on test set v1. See the README's *Scope* section.

**Limits.**
- The threshold is chosen on the same test set it is reported on.
- The test sets and the training data are built from the same kind of template: short, plain, particular answers. They share no phrase, but they share a style. Performance on answers people type in their own words is not measured.
- The artwork set has 24 real answers and the unseen set 96. Changes of one answer between versions (21 to 20 of 24, 59 to 61 of 96) say nothing on their own.
- Three pointings, averaged. One pointing alone moves the count by about thirty.
- *Nothing special.* counts as an answer to *Does it have any mark?* (margin 14.2), read as *no marks worth naming*; 0.3.5 refused it. On the other questions tried it is refused as before.
- English only. Answers mentioning Indian coins, places and brands appear throughout, because the templates were written in India, in Claude Code sessions.

**How to use it.**

```python
from rai.reader import Reader
r = Reader("prayasabhinav/rai")        # or a local folder
span, margin = r.read("What colour is it?", "Dark grey, with a rusty patch.", stem="It is ")
counted = span is not None and margin > 9.30
```

With plain transformers it behaves as any SQuAD 2.0 extractive model, but the threshold above only holds with rai's reading rule in `rai/reader.py`: the best span against the null answer, a span no longer than 30 tokens, and the span required to appear verbatim in the typed answer.

**Out of scope.** It does not grade, suggest or give reasons, and its margin is not shown to anyone. It is not for use as a step in a decision that affects somebody else.

**Licence.** CC-BY-4.0. Attribute Koher's rai reader, and deepset and Microsoft as above.
