# Changelog

## 0.3.6 — 25 September 2026

**The answers 0.3.6 trains on were written by Comma v0.1**, a model trained only on openly licensed and public-domain text. The questions and stems were written in Claude Code sessions, not by Comma, with a frontier model trained on other people's words, and the reader it is trained from, deepset's MiniLM fine-tuned on SQuAD 2.0, was not built from openly licensed text.

- **The answers rai trains on are written by Comma v0.1.** The phrases that answer each question, and the evasive, deferred and general replies that do not, were written by [Comma v0.1-2T](https://huggingface.co/common-pile/comma-v0.1-2t), a 7B model from EleutherAI and collaborators trained on openly licensed text (the Common Pile v0.1), run locally. Each phrase was read and judged before it was kept, against the question it answers and the thing the form is about: a little over half the phrases were kept, and one reply in three. Comma was shown the question, its stem, the thing the form is about, and phrases of its own already kept, never phrases from another source; naming the thing (*a cup of tea*, *a handful of gravel*) raised the share it wrote well. They are in `data/fill-comma.jsonl` (908 phrases over the 116 questions) and `data/nonanswers-comma.jsonl` (51 replies). The forms, their questions and stems, the empty answers and the recipe are unchanged, so the rows differ from 0.3.5's only in their words. No phrase names an animal product.
- **Measured on the same three test sets at one threshold, 9.30:** 161 of 180 honest answers on test set v1, 20 of 24 on the artwork set, and 61 of 96 on the unseen forms, with no non-answer counted in any. 0.3.5 counted 155, 21 and 59 at 12.67. A threshold belongs to the reader it was measured for, so the two are not comparable as numbers.
- **The reader is three readers averaged.** The same recipe pointed with seeds 7, 1 and 2 counted 223, 226 and 221 of 300; the average of their weights (a uniform model soup, Wortsman et al. 2022) counts 242, against 0.3.5's 235. One pointing alone moves the count by about thirty, so a single seed is no longer reported as the reader. `rai/train.py` takes `--seed`, `scripts/soup.py` averages and scores, and `scripts/train-full.sh` runs all of it.
- **`scripts/eval_reader.py --json`** writes each set's counts, the median margin of its honest answers, and the non-answer that sets the threshold.
- The trained reader is `rai-reader-0.3.6.tar.gz` on the release, and on Hugging Face as `prayasabhinav/rai`.

## 0.3.5 — 23 September 2026

- **rai counts more real answers on forms it was not trained on**: 59 of 96, where 0.3.4 counted 39. A probe on 23 September found 0.3.4 counting two of six real answers on a form it had never seen. 0.3.5 is trained on eight more forms, `call`, `repair`, `lost`, `ride`, `message`, `paperwork`, `door` and `screen`, and three training rows in ten reach the reader without their stem, honest answers and non-answers alike. The reader was retrained on 23,200 rows over nineteen forms.
- **A third test set, of forms the reader never trains on.** Four forms in `tests/unseen-forms/` and 168 rows in `tests/testset-unseen-v1.jsonl`, built by `scripts/build_unseen_testset.py`. `scripts/synth.py` stops if a training question repeats one of their questions, as it already stopped if a training row repeated a test phrase.
- **Measured on all three test sets at one threshold, 12.67:** 155 of 180 honest answers on test set v1, 21 of 24 on the artwork set, and 59 of 96 on the unseen forms, with no non-answer counted in any. 0.3.4, at the 16.24 that holds it at zero on all three, counted 138, 20 and 39. At its shipped 14.89, 0.3.4 counted two off-question answers on the unseen forms, which is why the comparison uses 16.24. A threshold belongs to the reader it was measured for, so 12.67 and 16.24 are not comparable as numbers.
- **No animal products.** The tea form asks *Soy milk and sugar — how much of each, or none?*, and every tea answer names soy milk. In other answers the walk form's milk booth and milk boy became a vegetable cart and a newspaper boy, a stone shaped like an egg became a flat oval, ink and gouache on silk became ink on paper, and a cream door became off-white. Test set v1 and the training data were regenerated from the same seeds; on the regenerated v1, 0.3.4 counts 138 of 180 at 16.24 where it counted 139 before.
- **`READER` beside `THRESHOLD`.** `rai/ask.py` names the current reader, `runs/rai-0.3.5`, next to the threshold measured for it. The contract test loads and reads with exactly that pair, and `tests/test_reader_v03.py` reads it by default. Programs built on rai can import both instead of copying a path and a number.
- The trained reader is `rai-reader-0.3.5.tar.gz` on the release, and on Hugging Face as `prayasabhinav/rai`.

## 0.3.4 — 22 September 2026

- **rai can check the record of an artwork.** An eleventh trained form, `wholes/artwork.yaml`: what it is made of, how big it is, who made it, when, what it is called, what marks are on it, where it is now and where it was before. The reader was retrained on 13,600 rows over the eleven forms.
- **Measured on two held-out test sets at one threshold, 14.89:** 146 of 180 honest answers on test set v1 (was 116), 20 of 24 on the new artwork set, and no non-answer counted in either.
- **The verbatim guard ignores spacing around punctuation.** The tokeniser writes "aunt's" as "aunt ' s", so correct answers containing an apostrophe were being refused. Nothing else is normalised, so the model still cannot add a word. On the 0.3.2 weights alone this lifted test set v1 from 116 to 122.
- **`scripts/check.sh`** runs every check that must pass before a change lands: the contract other programs rely on (`tests/test_contract.py`), the tally, the reader, and the guard that no training row repeats a test set.
- **`scripts/eval_reader.py` takes several test sets** and chooses one threshold over all of them.
- **`scripts/build_testset.py` runs again.** It imported a function that an earlier rewrite had removed. Repaired and checked: it reproduces test set v1 byte for byte.
- The reader now lives in `runs/rai-0.3.4`, so retraining no longer overwrites an older reader.

## 0.3.3 — 22 September 2026

- **Forms in Markdown.** A `.md` file in `wholes/` is now a form rai can run: `# name`, a numbered list of questions, an optional `- stem:` under each. `wholes/key.md` is an example. The ten shipped forms stay YAML, and the training and test scripts read only YAML, so an added form never reaches training.
- **The scope is stated.** The README opens with what kind of form rai is for, what is out of scope, and how far the trained reader reaches on forms it has not seen.
- **A detailed How to use**, with install steps for macOS, Linux and Windows, a checksum for the reader, and troubleshooting.
- The trained reader is unchanged; it is still `rai-reader-0.3.2.tar.gz` from release v0.3.2.

## 0.3.2 — 22 September 2026

The first public release.

- **The trained reader.** Trained further from deepset/minilm-uncased-squad2 on 12,000 synthetic pairs, two epochs, batch 32, on CPU. At a threshold of 14.56 it counts 116 of 180 honest answers in test set v1 and no non-answer.
- **The test set is held out.** `scripts/synth.py` removes every test-set phrase from its templates, including one that a stem would complete, and stops if a training row repeats the test set. An earlier internal build, 0.3.1, was trained on data sharing 153 of the test set's 180 honest answers; it was withdrawn before release and its figures are not reported here.
- **The threshold rounds up.** `scripts/eval_reader.py` chooses the threshold from unrounded margins and rounds it up, and `tests/test_reader_v03.py` fails if the threshold in `rai/ask.py` would let a non-answer through. Before this, a threshold rounded to two places could admit an answer whose margin sat just above it.
- **Complete means all seven notions pass.** The tally no longer adds a value per notion and compares a total; it checks that the set of notions passed is the seven. They are seven parts, not a sum.
- The interactive `count` command was removed. rai keeps two commands, `ask` and `tally`.
- The reader test defaults to `runs/rai-0.3-full`, the folder the release archive creates.

## Earlier internal versions

- **0.3.0** — the first trained reader, from two short CPU passes over 3,230 rows, and an interactive `count` command in the terminal, since removed.
- **0.2.0** — the untrained reader with a content-free stem per question, the verbatim guard, the margin threshold and the simple kind rule; the ten wholes and notions set 01.
- **0.1.0** — the tally, with no model; a person marks every question and notion by hand.
