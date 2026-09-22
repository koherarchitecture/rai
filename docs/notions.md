# The seven notions of completeness, set 01

A notion of completeness is a way a **description** can be complete. It is never a property of the thing described: a coin has no notions of completeness; a description of a coin does. All seven bear on the same one description at once.

Set 01 was frozen on 22 September 2026 and lives in `notions/set-01.yaml`. It will not be edited. Another set of seven can be added beside it later; `rai/whole.py` refuses a set that is not exactly seven.

| notion | a description is complete under it when | decided by | in code |
|---|---|---|---|
| declared parts | every question in the whole is answered | the reader and the tally | since 0.1.0 |
| answer kind | each answer is a checkable particular, or an owned position for a *why* | the kind rule | simple rule since 0.2.0 |
| two readers | every part is found by two independent readings; doubt is absence | two people, or a person and the reader | not yet |
| frame roles | inside each answer, every role its verb needs is filled: *submitted* needs by whom and to whom | a lexicon of verb frames, no model | not yet |
| conditions closed | every *when X* has its *when not X*; every failure named has its response | a rule over answers that carry a condition | not yet |
| no dangling names | every thing named in an answer is itself described somewhere | names matched against parts | not yet |
| nothing left to ask | a second person, given the description, has no question they still need before acting on it | the second person | not yet |

## How the seven combine

They do not add up. The seven are parts, and a description is complete when it passes all seven, in any order. There is no sequence and no hierarchy: none comes first, none outranks another. The table's order is only there so the notions can be named.

Six of seven is not complete, and neither is any other number short of seven. Which notions passed is never shown to anyone.

The `value` field on each notion in `notions/set-01.yaml` is the label it carried when the set was frozen. Values are never added.

## What complete means

Complete is a definition written in this file, not a fact about any description. rai's output means *complete under set 01* and nothing wider. Anyone who defines completeness differently can write their own set of seven.
