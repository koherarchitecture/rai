<p align="center">
  <img src="assets/rai-logo.svg" width="128" alt="rai: a mustard seed inside seven equal arcs">
</p>

<h1 align="center">rai</h1>

<p align="center"><strong>A model that checks if a set is complete.</strong></p>

<p align="center">
  <a href="https://github.com/koherarchitecture/rai/releases/tag/v0.3.3"><img src="https://img.shields.io/badge/release-v0.3.3-D59A3A" alt="release v0.3.3"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-AGPL--3.0-373E3C" alt="code licence AGPL-3.0"></a>
  <a href="LICENSE-WEIGHTS-AND-DATA.md"><img src="https://img.shields.io/badge/weights_%26_data-CC--BY--4.0-373E3C" alt="weights and data licence CC-BY-4.0"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB" alt="Python 3.10+">
  <a href="https://huggingface.co/prayasabhinav/rai"><img src="https://img.shields.io/badge/weights-Hugging_Face-FFD21E" alt="weights on Hugging Face"></a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/reader-extractive%2C_33M_parameters-E8B86D" alt="extractive reader, 33M parameters">
  <img src="https://img.shields.io/badge/runs_on-CPU-E8B86D" alt="runs on CPU">
  <img src="https://img.shields.io/badge/training_data-100%25_synthetic-E8B86D" alt="training data 100% synthetic">
  <img src="https://img.shields.io/badge/complete-all_seven_notions-E8B86D" alt="complete means all seven notions">
  <img src="https://img.shields.io/badge/output-one_word-E8B86D" alt="output is one word">
  <img src="https://img.shields.io/badge/logging-none-2E7D5B" alt="no logging">
  <a href="https://splitdomaincognition.org"><img src="https://img.shields.io/badge/follows-Split--Domain_Cognition-2E7D5B" alt="follows Split-Domain Cognition"></a>
</p>

---

rai checks whether a description answers every question of a form written in advance. It reads each typed answer with a small model and decides in plain code. It says one word: **complete** or **not complete**. It does not say what is missing, suggest wording or show a number.

The model in rai only points. Given a question and an answer, it returns the phrase in the answer that answers the question, or nothing. It cannot write a word of its own. Every decision after that is made by code short enough to read in a few minutes.

The name is the Hindi word for a mustard seed, राई, the proverbial smallest thing.

## Contents

- [Quick start](#quick-start)
- [Scope: the kind of set rai is for](#scope-the-kind-of-set-rai-is-for)
- [How to use](#how-to-use)
- [What it is for](#what-it-is-for)
- [Use cases](#use-cases)
- [How it works](#how-it-works)
- [The seven notions of completeness](#the-seven-notions-of-completeness)
- [The wholes](#the-wholes)
- [How well the reader reads](#how-well-the-reader-reads)
- [What rai will never do](#what-rai-will-never-do)
- [Model, data and training](#model-data-and-training)
- [Repository layout](#repository-layout)
- [Licences and credit](#licences-and-credit)

## Quick start

```bash
git clone https://github.com/koherarchitecture/rai.git
cd rai
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# the trained reader, 127 MB, from this release
curl -L -o rai-reader-0.3.2.tar.gz https://github.com/koherarchitecture/rai/releases/download/v0.3.2/rai-reader-0.3.2.tar.gz
mkdir -p runs && tar -xzf rai-reader-0.3.2.tar.gz -C runs/    # creates runs/rai-0.3-full/

.venv/bin/python -m rai ask wholes/stone.yaml
```

The reader can also be loaded straight from Hugging Face as `prayasabhinav/rai`; see [Use it from Python](#use-it-from-python).

Once the reader is downloaded, everything runs locally. Nothing you type is sent anywhere or kept after you quit.

| command | what it does |
|---|---|
| `python -m rai ask wholes/stone.yaml` | asks one whole's questions, reads each typed answer and decides notions 1 and 2 in code. The other five notions are not in code yet, so on its own it always ends *not complete*; it is a way to watch the reader work |
| `python -m rai tally wholes/stone.yaml` | the same tally with no model: a person marks each question and each notion by hand |

Tested with Python 3.12, torch 2.9 and 2.14, transformers 5.17, on macOS (Apple silicon) and Linux (ARM64).

## Scope: the kind of set rai is for

**rai is not a general completeness checker.** It checks one kind of set: a **fixed form**, a short list of questions written before anyone answers, where **every question asks for a concrete particular** and every answer is a **short typed phrase**.

- **A form** describes one thing or one event. The shapes are old ones: the catalogue fields of an object (colour, size, marks, where it came from), the circumstances of an event (what, where, when, how long, who), a recipe (what, how much, in what order, how long), an inventory (what, how many, where).
- **A particular** is something another person could check: a name, a number, a place, a time or a length of time, a colour, a comparison with a named thing, a mark and where it is.
- **An answer** is a phrase or a short sentence, typed as a person would say it: *Dark grey with a rusty patch.* *About ten minutes.* *The shared drive, in the Q3 folder.*
- **rai's question** about each answer is only: does it answer this question, and where? Never whether the answer is right, good or enough.

An example of a form in scope, one of the ten the reader was trained on:

> **a stone**
> 1. What colour is it?
> 2. How big is it, against a coin or your thumb?
> 3. What shape is it?
> 4. How does it feel — rough, smooth, cold, gritty?
> 5. Does it have any mark, crack, line or speck? Where?
> 6. Where did you pick it up?

**Out of scope:** judging quality, truth or sufficiency; questions whose answer is a reason, an opinion or an argument; long answers of more than a few sentences; free documents with no form behind them, such as proposals, essays or code; and any use where rai's word decides something for somebody other than the person who wrote the answers.

A form in scope that the reader was **not** trained on, and on which it does less well:

> **an equipment return**
> 1. What is being returned?
> 2. What condition is it in, and is there any damage? Where?
> 3. Is anything missing from it?
> 4. When was it taken out, and when is it being returned?
> 5. Where is it now?

**The trained domain is narrower than the scope.** The shipped reader was trained on ten forms. They cover all four shapes above (the stone and the coin are catalogue fields, the queue and the walk are circumstances, the tea is a recipe, the pocket is an inventory), but every one is about an everyday object or moment. The form can describe anything that fits the rules above; the reader has seen only these ten.

### How far the scope reaches, measured

The reader was trained, and tested, on the **60 questions of the ten shipped sets** and nothing else. Its figures hold for those questions. On sets it has not seen, it was tried on 22 September 2026 with real answers typed for each question:

| set | kind | real answers rai counted |
|---|---|---|
| the ten shipped sets (test set v1) | trained | 116 of 180 |
| a key (`wholes/key.md`) | unseen, close to the trained domain: an object | 4 of 6 |
| a handover note (three questions, not shipped) | unseen, further from it: circumstances of a piece of work | 1 of 3 |

In every case evasive answers (*Lots of things.*, *Not sure yet.*, *Somewhere.*) were refused. On a new set rai still refuses non-answers, but it misses more real ones, and so says *not complete* when the description is complete. The further a form is from the ten, the more it misses. Closing that gap needs training data from many more forms, and a test set of forms the reader has never seen. The threshold of 14.56 was also chosen on the ten, and is probably too strict for other forms. These are single tries, not measurements.

## How to use

### 1. Install

**What you need**

- **Python 3.10 or newer** (tested with 3.12). Check with `python3 --version` (Windows: `py --version`).
- **git**, to clone the repository.
- **About 1.5 GB of disk space**: PyTorch is most of it, the reader is 127 MB.
- **No GPU.** rai runs on an ordinary laptop CPU. No account, key or network connection is needed once it is installed.

**macOS and Linux**

```bash
git clone https://github.com/koherarchitecture/rai.git
cd rai
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/koherarchitecture/rai.git
cd rai
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

On Windows, use `.venv\Scripts\python` wherever this README says `.venv/bin/python`.

**Get the trained reader.** Download it from the release and extract it into `runs/`. On macOS and Linux:

```bash
curl -L -o rai-reader-0.3.2.tar.gz https://github.com/koherarchitecture/rai/releases/download/v0.3.2/rai-reader-0.3.2.tar.gz
shasum -a 256 rai-reader-0.3.2.tar.gz    # Linux: sha256sum
mkdir -p runs && tar -xzf rai-reader-0.3.2.tar.gz -C runs/
```

The checksum should read `9032c7580744ea938e76cbfba421933d6909c99460d00ddc71fd4aa7ca19c690`. You should end up with `runs/rai-0.3-full/model.safetensors`. On Windows (PowerShell), where `curl` alone means something else, use `curl.exe`:

```powershell
curl.exe -L -o rai-reader-0.3.2.tar.gz https://github.com/koherarchitecture/rai/releases/download/v0.3.2/rai-reader-0.3.2.tar.gz
Get-FileHash rai-reader-0.3.2.tar.gz -Algorithm SHA256    # prints the same hash in capitals
mkdir runs
tar -xzf rai-reader-0.3.2.tar.gz -C runs
```

The file can also be downloaded from the [release page](https://github.com/koherarchitecture/rai/releases/tag/v0.3.2) in a browser.

**Or load it from Hugging Face** instead of downloading by hand: pass `prayasabhinav/rai` wherever a model folder is asked for. It needs a connection the first time, then runs from the Hugging Face cache.

**Check the install**

```bash
.venv/bin/python tests/test_tally.py          # seven "ok" lines; no model needed
.venv/bin/python tests/test_reader_v03.py     # the trained reader on the test set
```

The second should end with `ok 0.3.0: does more than 0.2.0 by 100 honest answers; the shipped threshold 14.56 passes no non-counting answer`, meaning it finds 100 more real answers than the untrained reader and counts no evasive one.

**If something goes wrong**

| message | cause | fix |
|---|---|---|
| `no file named model.safetensors ... in directory runs/rai-0.3-full` | the reader is not extracted, or is in the wrong folder | extract the archive into `runs/` so that `runs/rai-0.3-full/model.safetensors` exists |
| `ModuleNotFoundError: No module named 'rai'` | Python was started outside the repository folder | run commands from inside `rai/`, or add the folder to `PYTHONPATH` |
| `ModuleNotFoundError: No module named 'torch'` | the virtual environment's Python was not used | use `.venv/bin/python`, not the system `python3` |
| `ensurepip is not available` when making the virtual environment | on Debian and Ubuntu, venv support is a separate package | `sudo apt install python3-venv`, then make the environment again |
| a long download on first use of `test_reader_v02.py` | that test uses deepset's untrained reader from Hugging Face | expected once; later runs use the cache |

### 2. Run a shipped set

```bash
.venv/bin/python -m rai ask wholes/stone.yaml
```

rai prints each question in turn; type an answer and press Enter. After the last answer it prints one word. For example:

```
— a stone —
What colour is it? Dark grey with a rusty patch.
How big is it, against a coin or your thumb? About the size of my thumbnail.
What shape is it? A wedge.
How does it feel — rough, smooth, cold, gritty? Rough and cold.
Does it have any mark, crack, line or speck? Where? A white speck near one end.
Where did you pick it up? The path behind the post office.
not complete
```

`ask` checks two of the seven notions of completeness in code and leaves the other five unmarked, so it always ends *not complete*; it is the way to watch the reader work. Step 5 shows how to mark the other five. `.venv/bin/python -m rai tally wholes/stone.yaml` runs the same tally with no model, marked by hand.

### 3. Write your own set in Markdown

Add a file ending in `.md` to `wholes/`. The format:

```markdown
# a key

One line saying what is being described. Any line that is not the title, a numbered question or a stem is a note and is ignored.

1. What is it made of, and what colour is it?
   - stem: It is made of
2. How long is it, against your finger?
   - stem: It is about as long as
3. Where is it right now?
   - stem: It is
```

- `# ` starts the name of the thing, once, at the top.
- Each question is a numbered line: `1.` or `1)`.
- `- stem:` under a question is optional: the words an answer usually starts with. It helps the reader find short answers and is never shown or counted. Keep it free of content (*It is made of*, never *It is made of plastic or*).
- Every question gets an equal share of the form. Nobody writes weights.

Stay inside the [scope](#scope-the-kind-of-set-rai-is-for): one thing or event, every question answered by a short particular. [`wholes/key.md`](wholes/key.md) is a complete example, and [`docs/wholes.md`](docs/wholes.md) has the rules that keep a question checkable. The ten shipped sets are YAML; both formats load the same way.

### 4. Run your set

```bash
.venv/bin/python -m rai ask wholes/key.md
```

### 5. Use it from Python

```python
from rai.reader import Reader
from rai.whole import load_whole
from rai.ask import read_answers
from rai.kind import counts
from rai.tally import word

reader = Reader("runs/rai-0.3-full")          # or "prayasabhinav/rai" from Hugging Face
whole = load_whole("wholes/stone.yaml")
answers = {"colour": "Dark grey with a rusty patch.", "size": "About the size of my thumbnail.",
           "shape": "A wedge.", "feel": "Rough and cold.", "marks": "A white speck near one end.",
           "from": "The path behind the post office."}

found = read_answers(whole, answers, reader)  # question id -> counted or not
passed = set()
if all(found.values()):
    passed.add("declared_parts")
if all(counts(a) for a in answers.values()):
    passed.add("answer_kind")
passed |= {"two_readers", "frame_roles", "conditions_closed", "no_dangling_names", "nothing_left_to_ask"}   # marked by people until they are in code
print(word(passed))                           # complete
```

Change the last answer about marks to *A chip on one corner.* and the same code prints *not complete*: the reader's margin for that answer is 6.12, under the threshold, so the part counts as absent. That is a false absent, the safe kind of error: whoever wrote the answers looks again.

`read_answers` applies the reader, the verbatim guard, the threshold and the kind rule together. `word` is the only thing that should reach a person.

rai is a model and a small library. Anything built on it calls it the same way and keeps its own interface.

The same code works for a Markdown set: `load_whole("wholes/key.md")`.

## What it is for

A description can sound finished and still leave out a part. People are bad at noticing the part that is not there, because a person fills a familiar gap without noticing it. A form, written down before anyone answers, turns that absence into something that can be checked: each question is either answered or not.

rai does that check with the model kept out of the verdict. The model is asked only where in an answer the reply to a question sits. What counts as an answer, and what complete means, is decided in code and in a YAML file anyone can read and change. The person who wrote the answers gets one word back and decides what to do with it.

## Use cases

| use | in short |
|---|---|
| Check a description against its form | write the form's questions once, answer them, tally; see the [scope](#scope-the-kind-of-set-rai-is-for) |
| Build on it | a program of your own that calls `read_answers()` and keeps its own interface |
| Your own sets | a Markdown file in `wholes/`, within the scope; see [How to use](#how-to-use) |
| A small benchmark | 360 labelled test answers and 12,000 training pairs for extractive readers |
| A worked example | a model limited to a small, checkable question, with every decision in readable code |

Examples, and what rai must never be used for, are in [`docs/use-cases.md`](docs/use-cases.md).

## How it works

```mermaid
flowchart LR
    A["A whole<br/>(fixed questions,<br/>written first)"] --> B["A person answers<br/>each question"]
    B --> C["Reader<br/>points at the phrase<br/>that answers, or at nothing"]
    C --> D["Kind rule<br/>particular, general,<br/>deferred or empty"]
    D --> E["Tally<br/>all seven notions?"]
    E --> F{{"complete<br/>or<br/>not complete"}}
    classDef lang fill:#E8B86D,stroke:#8E5E1C,color:#1f1f1f
    classDef code fill:#373E3C,stroke:#1f1f1f,color:#f5f0e6
    class C lang
    class D,E code
```

The work is split the way [Split-Domain Cognition](https://splitdomaincognition.org) describes: the model does language work, and the judgement lives in code anyone can read.

1. **A whole is a set of questions** about one thing, written before anyone answers. Each question has a short content-free stem (*It is …*, *It feels …*) that helps the reader and is never shown or counted. A question's weight is its share of 1 by position: six questions, one sixth each. See [`docs/wholes.md`](docs/wholes.md).
2. **The reader points.** For each question, a 33-million-parameter extractive model finds the phrase in the typed answer that answers it and gives a margin: how far its best phrase beats the choice of *no answer*. The phrase must appear in what was typed, word for word, or it does not count. The margin must clear a fixed threshold, 14.56. See [`rai/reader.py`](rai/reader.py).
3. **A kind rule in plain code** decides whether the answer is a checkable particular or something that does not count: deferred (*not sure*, *later*), general (*lots of things*, *the usual*) or empty. See [`rai/kind.py`](rai/kind.py).
4. **The tally** checks the seven notions of completeness. A description is **complete when it passes all seven**, in any order. They are seven parts, not a sum: nothing is added up and no value is kept. Anything short of all seven is *not complete*, and which notions passed is never shown. See [`rai/tally.py`](rai/tally.py).

Any doubt counts as absence. If the reader is unsure of a phrase, if an answer hedges, or if a question is left blank, the result is *not complete*.

Full detail in [`docs/how-it-works.md`](docs/how-it-works.md).

## The seven notions of completeness

A notion of completeness is a way a **description** can be complete. It is never a property of the thing described. All seven bear on the same one description at once.

| notion | a description is complete under it when | decided in this release by |
|---|---|---|
| declared parts | every question in the whole is answered | the reader and the tally |
| answer kind | each answer is a checkable particular, or an owned position for a *why* | the kind rule (particulars only in this release) |
| two readers | every part is found by two independent readings; doubt is absence | a person |
| frame roles | inside each answer, every role its verb needs is filled | a person |
| conditions closed | every *when X* has its *when not X*; every failure named has its response | a person |
| no dangling names | every thing named in an answer is itself described somewhere | a person |
| nothing left to ask | a second person, given the description, has no question they still need | a person |

The seven have no order and no rank. **Complete means all seven.** That rule is written down in [`notions/set-01.yaml`](notions/set-01.yaml), and rai's output means *complete under set 01* and nothing wider. Set 01 is frozen; another set of seven can be added beside it. See [`docs/notions.md`](docs/notions.md).

## The wholes

Ten wholes ship with rai, each about an everyday object or moment:

| whole | the thing |
|---|---|
| `stone` | one stone in your hand |
| `handful` | a handful of gravel, counted |
| `coin` | one coin from your pocket |
| `leaf` | one leaf |
| `queue` | a queue you stood in |
| `wait` | a wait |
| `tea` | the tea you last made |
| `walk` | the walk to the shop or the stop |
| `pocket` | what is in your pocket or bag |
| `sound` | a sound you can hear now |

Every question can be answered with a particular: a colour, a count, a comparison with a coin or a thumb, a place, a length of time. *How big is it?* has no checkable answer; *how big, against a coin?* does. A whole is a YAML file, and anyone can write one. The format and its rules are in [`docs/wholes.md`](docs/wholes.md).

## How well the reader reads

Measured on test set v1: 360 answers to the wholes' questions, 180 that answer honestly and 180 that do not (120 evasive, 60 answering a different question). No phrase in the test set appears anywhere in the training data, and `scripts/synth.py` stops if any training row repeats one.

| reader | threshold | non-answers counted as answers | honest answers counted |
|---|---|---|---|
| deepset/minilm-uncased-squad2, not trained further, with stems (0.2.0) | 10.60 | 0 of 180 | 16 of 180 |
| **rai reader 0.3.2** | **14.56** | **0 of 180** | **116 of 180** |

By class, at 14.56: 116 of the 180 honest answers counted; all 120 evasive and all 60 off-question answers refused.

What these numbers do and do not say:

- **The threshold is chosen on the same test set it is reported on.** It is the smallest margin that lets no non-answer through. A threshold chosen on one set and tested on another is planned for a later version, and until then the zero in the middle column is a property of this set.
- **The test set and the training data come from the same kind of template.** They share no phrase, but they share a style: short, plain, particular answers about the same ten things. How the reader does on answers people actually type, in their own words, is not yet measured.
- **These figures cover the ten shipped sets only.** On sets it has not seen, rai misses more real answers; see [How far the scope reaches](#how-far-the-scope-reaches-measured).
- **One training run, one seed.**
- **A false present is the error that matters most.** Counting a non-answer as an answer can turn *not complete* into *complete*. A false absent only sends the person who wrote the answers back to look again.

Reproduce: `python scripts/eval_reader.py tests/testset-v1.jsonl runs/rai-0.3-full`.

## What rai will never do

- Say why a description is not complete, or what is missing.
- Suggest wording, or write a word of its own.
- Show a score, a fraction or a percentage.
- Keep anything anybody types, or count who uses it.
- Claim more than *complete under set 01*.
- Be used as a step in a decision that affects somebody else, such as an application or an assessment. Its word is for the person who wrote the answers.

## Model, data and training

- **The reader** is a question-answering model trained further from [deepset/minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2), itself deepset's fine-tune of Microsoft's [MiniLM-L12-H384-uncased](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) on SQuAD 2.0. Same architecture, 33M parameters, nothing added. [`MODEL-CARD.md`](MODEL-CARD.md)
- **The training data** is 12,000 synthetic question-and-answer pairs made from templates by [`scripts/synth.py`](scripts/synth.py), seeded, with labels known by construction. It contains nobody's words. [`DATA-CARD.md`](DATA-CARD.md)
- **To train it again**, on a CPU: `PYTHON=.venv/bin/python bash scripts/train-full.sh`. It regenerates the data, trains for two epochs at batch 32, and runs the test. About eight minutes on 18 ARM cores; nearer an hour on a 5-core laptop.

## Repository layout

```
rai/            the package: reader, kind rule, tally, the two commands, training
notions/        set-01.yaml, the seven notions of completeness
wholes/         ten question sets, one YAML file each
scripts/        synth.py (training data), build_testset.py, eval_reader.py, train-full.sh
tests/          tally tests, reader tests, test set v1, recorded results
data/           train-synth.jsonl, the 12,000 training pairs
docs/           how it works, use cases, the notions, the wholes
assets/         the rai mark and the Koher logo
```

Run the tests:

```bash
.venv/bin/python tests/test_tally.py
.venv/bin/python tests/test_reader_v02.py          # the untrained reader; downloads it once
.venv/bin/python tests/test_reader_v03.py          # the trained reader in runs/rai-0.3-full
```

## Licences and credit

- **Code:** GNU AGPL-3.0, in [`LICENSE`](LICENSE).
- **Weights and training data:** CC-BY-4.0, in [`LICENSE-WEIGHTS-AND-DATA.md`](LICENSE-WEIGHTS-AND-DATA.md).
- **Built on:** deepset's [minilm-uncased-squad2](https://huggingface.co/deepset/minilm-uncased-squad2) (CC-BY-4.0) and Microsoft's [MiniLM](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased) (MIT). Both are credited here and in the model card, as their licences ask.
- **The idea:** the split between reading and deciding comes from [Split-Domain Cognition](https://splitdomaincognition.org), a principle that is nobody's property.

To cite rai, see [`CITATION.cff`](CITATION.cff).

---

<p>
  <a href="https://koher.app"><img src="assets/koher-logo.svg" width="40" alt="Koher" align="left"></a>
  rai is made by <a href="https://koher.app">Koher</a>, a practice building free AI tools that keep judgement in code anyone can read.
</p>
