---
license: cc-by-4.0
language:
- en
- hi
library_name: transformers
pipeline_tag: question-answering
base_model: deepset/minilm-uncased-squad2
tags:
- extractive-question-answering
- completeness
- split-domain-cognition
- synthetic-data
- cpu
- hinglish
- code-mixed
---

# rai reader 0.3.8 — model card

**What it is.** An extractive question-answering model. Given a question and a short typed answer, it returns the phrase in the answer that answers the question, or nothing. It cannot generate text. It is the reading part of [rai](https://github.com/koherarchitecture/rai), a tool that says only whether a description is complete under a notion of completeness written down in advance. Every decision after the reading is made in plain code.

**Trained from.** [deepset/minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2) (CC-BY-4.0), deepset's fine-tune of Microsoft's [MiniLM-L12-H384-uncased](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) (MIT) on SQuAD 2.0. Same architecture, 33M parameters, nothing added. Credit to deepset and Microsoft.

**0.3.8 also counts some answers typed in Hinglish** (27 of 58 on the Hinglish test set, against 152 of 180 in English on test set v1). It is the average of two readers' weights, 0.4 of 0.3.7 and 0.6 of a reader taught Hinglish by a larger model (described below); since both start from deepset's MiniLM, the average is a reader of the same size. The teacher, HingBERT ([l3cube-pune/hing-bert](https://huggingface.co/l3cube-pune/hing-bert), CC-BY-4.0, by L3Cube Pune, Nayak and Joshi 2022, whom this release credits), is BERT-base trained further on romanised Hinglish; it is not shipped.

**0.3.7, the other reader in the average, trains on 0.3.6's rows and 5,800 more written in Claude Code.** In 0.3.6's rows the answers were written by Comma v0.1, a model trained only on openly licensed and public-domain text, and the questions and stems in Claude Code sessions. The new rows, questions and answers both, were written in Claude Code, with a frontier model trained on other people's words. The reader it is trained from, deepset's MiniLM fine-tuned on SQuAD 2.0, was not built from openly licensed text.

**Trained on.** 29,000 synthetic pairs, labels known by construction. 23,200 are 0.3.6's, over nineteen forms, made by `scripts/synth.py` (seed 7): honest answers given bare or after the question's stem, and evasive, deferred, general, empty and off-question answers labelled *no answer*, three rows in ten without their stem. 5,800 are new, made by `scripts/synth_live.py` (seed 37): questions as people write them, with no stem, answered with the kind of thing each asks for (a person, a place or an errand, a time, a number, a brand, a food, what a verb takes, what makes a noise, an Indian name), half typed the way people type, with wrong-kind answers labelled *no answer*. No person's answers are in it, and no animal product is named, by Koher's rule for every model it trains. Two epochs, batch 32, learning rate 2e-5, maximum length 384, about 3 minutes a seed on a Mac's GPU. The recipe was run with seeds 7, 1 and 2 and the three readers' weights averaged into this one (a uniform model soup, Wortsman et al. 2022). See `DATA-CARD.md`.

**The Hinglish reader.** It is deepset's MiniLM trained on the same 29,000 rows plus 5,800 Hinglish rows from `scripts/synth_hinglish.py` (seed 38, written in Claude Code). The Hinglish rows answer questions in English or Hinglish about a person, a place, a time, a count, a length of time, a colour, a material, a price, an object or a sound, with the words people put around an answer (*Ramesh ne kiya*, *store room mein rakha hai*). Vague, evasive and wrong-kind answers are labelled *no answer*. On the Hinglish rows the reader was also trained to match the teacher's start and end scores. Both sets of scores were first rescaled, each row's to mean 0 and spread 1 (Sun et al. 2024), and matched by squared difference (Kim et al. 2021). Matching the raw scores instead gave vague answers large margins, and the threshold needed to keep them out let almost no real answer through. The teacher was taught SQuAD 2.0 and then the same rows. Seeds 7, 1 and 2, averaged. Without the average it counted 34 of 58 Hinglish answers but only 102 of 131 Indian names asked about with *who*; averaged with 0.3.7 it keeps 125 of them. `scripts/train-full.sh` runs every step.

**Measured, 0.3.7** on six test sets it never trained on, at one threshold, **8.92**, the smallest margin that lets no non-answer through in any of them, with rai's two kind rules applied (`rai/kind.py`, `rai/fit.py`): **157 of 180** on test set v1, **20 of 24** on the artwork set, **66 of 96** on the unseen forms (33 of 48 with the form's stem, 33 without), **52 of 60** on rai ka pahad rounds, and **21 of 24** and **44 of 46** on two sets of people's typing. It counts no non-answer in any set. 0.3.6, scored the same way, counted 161, 20, 62, 42, 4 and 1. On three probes written before the last training and never trained on: 20 of 20 in a batch of people's typing, 120 of 123 Indian names that no training row contains, and 17 of 20 answers that mean the right thing in free wording, with one non-answer counted (*the peon* for what was being photocopied). No answer in any test set appears in the training data.

**Measured, 0.3.8** on seven test sets at one threshold, **11.53**, with both kind rules, which from 0.3.8 also refuse vague and judging Hinglish answers (*koi*, *kisi ke paas hogi*, *sab kuch*, *sasta tha*): **152 of 180** on test set v1, **18 of 24** on the artwork set, **64 of 96** on the unseen forms, **48 of 60** on rai ka pahad rounds, **21 of 24** and **42 of 46** on the typing sets, and **27 of 58 on the Hinglish set**, where 0.3.7 counts 16. It counts no non-answer in any set. Probes, re-scored on both readers with one pairing over all 131 names in the file (the 0.3.7 figures above used 123): 125 of 131 Indian names counted for *who* (0.3.7: 127) and none for *where* or *when*; 16 of 20 free-worded meanings with one non-answer counted; 20 of 20 in the last batch of people's typing.

**Scope.** The reader is for forms: a short list of questions written in advance, each asking for a concrete particular (a name, a number, a place, a time, a colour, a comparison with a named thing), answered in short typed phrases. It is not a general completeness checker and does not judge whether an answer is right or enough. It was trained on nineteen forms: eighteen about everyday objects, moments and events, and the record of an artwork. On forms it was not trained on it refuses non-answers as before but misses more real ones, 66 of 96 on the unseen set against 157 of 180 on test set v1. See the README's *Scope* section.

**Limits.**
- The threshold is chosen on the same test set it is reported on.
- Every test answer was written in Claude Code, including the people's-typing sets, which stand in for people. They share no phrase with the training data. Performance on rounds written by people who use rai is not measured.
- It still counts one kind of wrong answer in the probes: a person given for a *what* (*the peon* for what was being photocopied).
- The smaller sets have 24 to 96 real answers. A change of one or two answers between versions says nothing on its own.
- Three pointings, averaged. One pointing alone moves the count by about thirty.
- *Nothing special.* counts as an answer to *Does it have any mark?* (margin 14.2), read as *no marks worth naming*; 0.3.5 refused it. On the other questions tried it is refused as before.
- English and Hinglish typed in Roman letters, not Devanagari. Hinglish is read less well than English: 27 of 58 honest Hinglish answers against 152 of 180 on test set v1. The Hinglish set's answers were written in Claude Code and its labels checked by one Hindi speaker.
- English with Indian names, words (*ji*, *di*, *garu*, *chettan*) and places throughout, because the templates were written in India, in Claude Code sessions.

**How to use it.**

```python
from rai.reader import Reader
r = Reader("prayasabhinav/rai")        # or a local folder
span, margin = r.read("What colour is it?", "Dark grey, with a rusty patch.", stem="It is ")
counted = span is not None and margin > 11.53   # rai also applies rai/kind.py and rai/fit.py
```

With plain transformers it behaves as any SQuAD 2.0 extractive model, but the threshold above only holds with rai's reading rule in `rai/reader.py`: the best span against the null answer, a span no longer than 30 tokens, and the span required to appear verbatim in the typed answer; and rai's two kind rules, `rai/kind.py` and `rai/fit.py`, which the threshold was measured with.

**Out of scope.** It does not grade, suggest or give reasons, and its margin is not shown to anyone. It is not for use as a step in a decision that affects somebody else.

**Licence.** CC-BY-4.0. Attribute Koher's rai reader, and deepset, Microsoft and L3Cube as above.
