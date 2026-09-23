# The wholes, and how to write one

A whole, or form, is the set of questions that make up a complete description of one thing or event. rai ships nineteen. They are the reader's training domain: descriptions of everyday objects, moments and events, and the record of an artwork, each built on an older descriptive form.

| file | the thing |
|---|---|
| `stone.yaml` | one stone in your hand |
| `handful.yaml` | a handful of gravel, counted |
| `coin.yaml` | one coin from your pocket |
| `leaf.yaml` | one leaf |
| `queue.yaml` | a queue you stood in |
| `wait.yaml` | a wait |
| `tea.yaml` | the tea you last made |
| `walk.yaml` | the walk to the shop or the stop |
| `pocket.yaml` | what is in your pocket or bag |
| `sound.yaml` | a sound you can hear now |

Each descends from an older way of making a description complete: the circumstances of an event (who, what, where, when, how long), a recipe, an inventory, or a museum's catalogue fields for an object (colour, size, marks, where it was found).

## Writing a set in Markdown

The simplest way to add a set: a `.md` file in `wholes/`.

```markdown
# a key

A note line, ignored by rai.

1. What is it made of, and what colour is it?
   - stem: It is made of
2. How long is it, against your finger?
   - stem: It is about as long as
```

`# ` names the thing. Numbered lines (`1.` or `1)`) are the questions. An indented `- stem:` under a question is optional. Every other line is ignored. `wholes/key.md` is a full example. rai's reader was trained on the nineteen shipped sets only, so a new set works best when it is close to them: one thing or event, every question answered by a short particular.

## The YAML format

The nineteen shipped sets are YAML, and carry two fields the Markdown format leaves out for the person writing the set.

```yaml
notion: a coin
kind_rule: simple
questions:
  - id: value
    text: "What is it worth, and what is written on it?"
    stem: "It is a "
    kind: fact
    counts_when: "a stated value, and a word or number on it"
```

| field | meaning |
|---|---|
| `notion` | the thing being described |
| `kind_rule` | which kind rule applies; `simple` in this release |
| `id` | a short name for the question |
| `text` | the question as it is read aloud |
| `stem` | the words an answer usually starts with; helps the reader, never shown |
| `kind` | `fact`, or `why` for a question about a reason |
| `counts_when` | what an answer that counts looks like, for the person writing the whole |

Weights are never written. A question's weight is its share of 1 by position.

## Rules every question follows

1. **One thing per question.** *Where and when* is two questions, unless an answer to either half alone would count.
2. **It can be answered with a particular**: a name, a number, a place, a colour, a named thing, a length of time. A question that can only be answered with a quality, such as *is it good?*, is not allowed. The reader cannot check a quality and rai never judges one.
3. **Specific, not general.** *How big is it, against a coin?* rather than *How big is it?* A comparison gives a vague property a checkable answer.
4. **Say what the question is about**, in the question: *Who uses it?*, not *Who?*
5. **Never leading.** A question must not carry an assumption the person cannot reject. The stem is content-free for the same reason: *It is made of* is a stem; *It is made of plastic or* is a suggestion.
6. **Plain words.** No technical terms, which people read differently from the writer.
7. **A why counts only as an owned position.** An answer to a `why` question counts when it is stated as the writer's own view (*I think … because …*).
8. **The plain fact first.** What the thing is comes before anything else in the order.

## What no whole asks

A rating, a preference, a comparison with somebody else, or whether anything is good. No whole asks about a person's work or performance.
