# Changelog

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
- The terminal pastime moved to its own project, which calls rai. rai keeps two commands, `ask` and `tally`.
- The reader test defaults to `runs/rai-0.3-full`, the folder the release archive creates.

## Earlier internal versions

- **0.3.0** — the first trained reader, from two short CPU passes over 3,230 rows, and a terminal pastime for two that has since become its own project.
- **0.2.0** — the untrained reader with a content-free stem per question, the verbatim guard, the margin threshold and the simple kind rule; the ten wholes and notions set 01.
- **0.1.0** — the tally, with no model; a person marks every question and notion by hand.
