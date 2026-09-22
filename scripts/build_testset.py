"""Test set v1: for every question of every whole, bare answers that count and answers that do not, labels known by construction.
Writes tests/testset-v1.jsonl. Seeded; things named are plain and real."""
import json, os, random, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rai.whole import load_whole
from synth import fill_for   # off-question rows must cross kinds, or the 'wrong' answer answers both questions

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(22)

# real answers per question, bare, as people say them (one line each)
REAL = {
 "stone/colour": ["Grey with a white band.", "Dark brown.", "Reddish, darker at one end."],
 "stone/size": ["About the size of a two-rupee coin.", "A bit bigger than my thumbnail.", "Half my palm."],
 "stone/shape": ["Like an egg, flattened.", "A rough triangle.", "Round, like a laddoo."],
 "stone/feel": ["Smooth on one side, gritty on the other.", "Cold and rough.", "Smooth all over."],
 "stone/marks": ["A white line across the middle.", "A small chip on one corner.", "None."],
 "stone/from": ["The path outside the library.", "Sabarmati riverfront, near the steps.", "The parking lot at college."],
 "handful/count": ["Fourteen.", "Twenty-two pieces.", "Nine."],
 "handful/biggest": ["One about the size of a peanut.", "The biggest is as big as a ten-rupee coin.", "A flat one, thumbnail size."],
 "handful/smallest": ["Like a mustard seed.", "A grain of rice.", "Smaller than a peppercorn."],
 "handful/colours": ["Nine grey, four brown, one white.", "All grey except two black.", "Mostly brown, three reddish."],
 "handful/odd": ["One is black and shiny, the rest are dull grey.", "One is round, the others are broken.", "None, they are all alike."],
 "handful/from": ["The edge of the cricket ground.", "The driveway at home.", "A construction pile on the road outside."],
 "coin/value": ["Two rupees, it says Bharat and two.", "A ten-rupee coin.", "One rupee, with the lion."],
 "coin/year": ["2019.", "It says 2011.", "None visible, it is too worn."],
 "coin/sides": ["The lion capital on one side, the number two on the other.", "Ashoka pillar on one side, ten with the rays on the other.", "A thumbs-up hand on one side, the lions on the other."],
 "coin/wear": ["Dull, with scratches on the number side.", "Shiny, almost new.", "Worn smooth at the rim."],
 "coin/from": ["Change from the tea stall this morning.", "The auto driver gave it as change.", "My mother's purse."],
 "coin/now": ["In my left pocket.", "On the desk next to the keyboard.", "In the pen stand."],
 "leaf/plant": ["A neem tree.", "The peepal outside the gate.", "Tulsi from the pot on the balcony."],
 "leaf/size": ["As long as my little finger.", "Bigger than my palm.", "About as wide as two fingers."],
 "leaf/colour": ["Green, yellow at the edges.", "Dark green all over.", "Brown, with green near the stem."],
 "leaf/edge": ["Toothed like a saw.", "Smooth.", "Torn on one side."],
 "leaf/marks": ["Two holes near the tip.", "Black spots along the vein.", "None."],
 "leaf/where": ["On the footpath under the tree.", "Still on the branch, I picked it.", "On the bonnet of the car."],
 "queue/where": ["The canteen counter.", "The bank on CG Road.", "The bus stop at Paldi."],
 "queue/for": ["Tea and a vada pav.", "To deposit a cheque.", "The 52 bus."],
 "queue/ahead": ["Six people.", "About fifteen.", "Two."],
 "queue/long": ["Ten minutes.", "Half an hour.", "Three or four minutes."],
 "queue/front": ["A woman with a red bag.", "Two students from my class.", "An old man with a walking stick."],
 "queue/did": ["Looked at my phone.", "Counted the tiles on the floor.", "Talked to the person behind me."],
 "wait/where": ["At the lift on the third floor.", "The bus stop outside the campus.", "In the car at the railway crossing."],
 "wait/for": ["The lift.", "The 41 bus.", "The train to pass."],
 "wait/long": ["Four minutes.", "About twenty minutes.", "Nearly an hour."],
 "wait/looked": ["The floor numbers going up and down.", "A hoarding for a jewellery shop.", "The gate man's chair."],
 "wait/did": ["Held my bag strap.", "Nothing, they were in my pockets.", "Scrolled on the phone."],
 "wait/ended": ["The lift came.", "The bus arrived and I got on.", "The train passed and the gate opened."],
 "tea/water": ["One cup.", "Two cups of water.", "Half a litre."],
 "tea/tea": ["Two spoons of Wagh Bakri.", "One teabag, Red Label.", "One and a half spoons of loose tea."],
 "tea/milk": ["Half a cup of milk, one spoon of sugar.", "No milk, two sugars.", "A splash of milk, no sugar."],
 "tea/steps": ["Boiled the water, added tea, then milk, then sugar, strained it.", "Water and tea together, boiled twice, milk at the end.", "Teabag in the cup, poured the water, left it three minutes, added milk."],
 "tea/time": ["Seven minutes.", "About five minutes.", "Ten minutes, the milk took time."],
 "tea/done": ["When it turned dark brown and rose up once.", "When the colour was right, like the tea stall's.", "When it boiled over the second time."],
 "walk/ends": ["From my flat to the Reliance Fresh on the corner.", "From the hostel gate to the bus stop.", "From the office to the chai stall."],
 "walk/time": ["Six minutes.", "About ten minutes.", "Three minutes."],
 "walk/pass": ["The temple, the tyre shop, then the school gate.", "A paan shop, then the park.", "The society gate, the garbage bin, the milk booth."],
 "walk/underfoot": ["Paver blocks, broken in places.", "Tar road.", "Mud and gravel."],
 "walk/see": ["The watchman and the milk boy.", "Nobody, usually.", "The same two dogs."],
 "walk/instead": ["Go round by the main road.", "Take the auto.", "Wait till it clears."],
 "pocket/list": ["Keys, a pen, the phone, a folded bus ticket.", "Phone, wallet, an earphone case.", "A handkerchief, two coins, the ID card."],
 "pocket/count": ["Four things.", "Three.", "Five."],
 "pocket/oldest": ["The keys, since I moved in, 2023.", "The wallet, three years.", "The ID card, since first year."],
 "pocket/heaviest": ["The phone.", "The keys.", "The wallet."],
 "pocket/miss": ["The keys.", "The phone.", "The ID card."],
 "pocket/night": ["On the shelf by the door.", "In the drawer.", "On the table next to the bed."],
 "sound/what": ["The ceiling fan.", "A drill from the next building.", "Crows outside."],
 "sound/where": ["Above me.", "From the left, across the road.", "The window behind me."],
 "sound/pattern": ["Steady.", "It stops and starts.", "One-off, every few minutes."],
 "sound/loud": ["About as loud as a fridge.", "Louder than the traffic.", "Quieter than my own typing."],
 "sound/since": ["Since I came in this morning.", "About ten minutes.", "Since the power came back."],
 "sound/stops": ["When I switch it off.", "When they finish the wall.", "When the sun goes down."],
}

EVASIVE = ["It is really nice.", "Hard to say.", "Not sure.", "The usual.", "A lot of things.", "It works well.",
           "I don't know yet.", "Whatever is there.", "Something, I guess.", "Maybe later."]

rows = []
for path in sorted(glob.glob(os.path.join(HERE, "wholes", "*.yaml"))):
    w = load_whole(path)
    name = os.path.basename(path)[:-5]
    for q in w["questions"]:
        key = f"{name}/{q['id']}"
        reals = REAL.get(key, [])
        for a in reals:
            rows.append({"whole": name, "qid": q["id"], "question": q["text"], "stem": q.get("stem", ""), "answer": a, "label": True, "class": "bare"})
        for a in random.sample(EVASIVE, 2):
            rows.append({"whole": name, "qid": q["id"], "question": q["text"], "stem": q.get("stem", ""), "answer": a, "label": False, "class": "evasive"})
        # off-question: a real answer to another question of the same whole
        qkind = {f"{name}/{o['id']}": fill_for(o['counts_when']) for o in w['questions']}
        others = [k for k in REAL if k.startswith(name + "/") and k != key and qkind.get(k) != qkind[key]]
        if others and reals:
            k = random.choice(others)
            rows.append({"whole": name, "qid": q["id"], "question": q["text"], "stem": q.get("stem", ""), "answer": random.choice(REAL[k]), "label": False, "class": "off-question"})

out = os.path.join(HERE, "tests", "testset-v1.jsonl")
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "rows;", sum(r["label"] for r in rows), "count,", sum(not r["label"] for r in rows), "do not")
