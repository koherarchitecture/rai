"""The unseen-forms test set: four forms the reader is never trained on, in tests/unseen-forms/, so a reader is measured on
questions it has not seen as well as on answers it has not seen. Added for 0.3.5 on 23 September 2026, after a probe found
0.3.4 counting two of six plainly particular answers on a form it had never met. For every question: two honest answers
read with the form's stem and again with none, one evasive answer each way, and one answer to another question of the same
form. Labels by construction; nothing random. The honest answers were written for this set, not collected from people
who have used rai; a set written by such people is still owed. Writes tests/testset-unseen-v1.jsonl."""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL = {
 "search/app": [
  "IRCTC, on my phone.",
  "The electricity board's website."
 ],
 "search/find": [
  "The cancellation charge for a waitlisted ticket.",
  "The due date on my last bill."
 ],
 "search/first": [
  "The My Transactions menu.",
  "The top menu, under Services."
 ],
 "search/tapped": [
  "Booked Ticket History, then Cancel Ticket.",
  "I typed my consumer number into the search box."
 ],
 "search/long": [
  "About twelve minutes.",
  "Twenty minutes, with the page reloading twice."
 ],
 "search/ended": [
  "I found the charges in a PDF linked at the bottom of the FAQ page.",
  "My neighbour told me the date."
 ],
 "rain/where": [
  "On the scooter, halfway to college.",
  "At the bus stop near the stadium."
 ],
 "rain/carrying": [
  "My laptop bag and a packet of vegetables.",
  "Just my phone."
 ],
 "rain/shelter": [
  "Under the flyover.",
  "In the doorway of a hardware shop."
 ],
 "rain/stayed": [
  "About fifteen minutes.",
  "Till the rain slowed, maybe half an hour."
 ],
 "rain/home": [
  "By auto, soaked.",
  "I walked the last bit with a plastic bag over my head."
 ],
 "rain/wet": [
  "My shoes and the left side of my bag.",
  "Everything except the phone, which was in a pouch."
 ],
 "bottle/material": [
  "Steel.",
  "Blue plastic, a bit scratched."
 ],
 "bottle/holds": [
  "One litre.",
  "About half a litre."
 ],
 "bottle/fill": [
  "At the water cooler outside the library.",
  "From the filter at home."
 ],
 "bottle/side": [
  "My name, in marker pen.",
  "The name of a bike shop."
 ],
 "bottle/cap": [
  "A flip-top with a straw.",
  "A screw cap on a little chain."
 ],
 "bottle/age": [
  "Two years.",
  "Since the start of this term."
 ],
 "charger/where": [
  "At the hospital, waiting for a report.",
  "In the metro, two stops from home."
 ],
 "charger/doing": [
  "Paying for groceries with UPI.",
  "A video call with my aunt."
 ],
 "charger/charged": [
  "With a power bank a friend lent me.",
  "At a charging point in the waiting hall."
 ],
 "charger/whose": [
  "The shopkeeper's charger.",
  "My own, from my bag."
 ],
 "charger/long": [
  "About ten minutes.",
  "Nearly half an hour."
 ],
 "charger/missed": [
  "Two calls from my mother.",
  "The OTP for the payment."
 ]
}
# questions of one form whose answers can legitimately swap: never used as off-question pairs for each other
EXCHANGEABLE = [['search/first', 'search/tapped'], ['rain/shelter', 'rain/where'], ['charger/charged', 'charger/whose']]
# evasions that appear nowhere in scripts/synth.py, so holding them out takes nothing away from training
EVASIVE = ["No idea, honestly.", "Couldn't say.", "Whatever it was.", "Can't remember now.", "Just the usual thing.", "Some stuff.",
           "Kind of everywhere.", "Hmm, not really sure.", "Don't remember.", "All kinds of things.", "It's hard to explain.", "Nothing much."]

rows, e = [], 0
for path in sorted(glob.glob(os.path.join(HERE, "tests", "unseen-forms", "*.yaml"))):
    name = os.path.basename(path)[:-5]
    qs = load_whole(path)["questions"]
    keys = [f"{name}/{q['id']}" for q in qs]
    for i, (q, k) in enumerate(zip(qs, keys)):
        base = dict(whole=name, qid=q["id"], question=q["text"])
        for a in REAL[k]:
            rows.append(dict(base, stem=q["stem"], answer=a, label=True, **{"class": "bare"}))
            rows.append(dict(base, stem="", answer=a, label=True, **{"class": "bare-nostem"}))
        rows.append(dict(base, stem=q["stem"], answer=EVASIVE[e % 12], label=False, **{"class": "evasive"}))
        rows.append(dict(base, stem="", answer=EVASIVE[(e + 5) % 12], label=False, **{"class": "evasive-nostem"}))
        e += 1
        other = next(keys[j] for j in list(range(i + 1, len(keys))) + list(range(i)) if not any({k, keys[j]} <= set(g) for g in EXCHANGEABLE))
        rows.append(dict(base, stem=q["stem"], answer=REAL[other][0], label=False, **{"class": "off-question"}))

out = os.path.join(HERE, "tests", "testset-unseen-v1.jsonl")
with open(out, "w") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "rows", dict(Counter(r["class"] for r in rows)), "->", out)
