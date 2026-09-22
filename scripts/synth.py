"""100% synthetic training pairs, labels by construction. Writes data/train-synth.jsonl.
Row: question, stem, answer, span (the phrase that answers, or null), class. Templates only, seeded; every particular is a plain real thing.
Rewritten 22 September 2026: fillers are written PER QUESTION and phrased to follow that question's stem, after ten sampled rows showed
a keyword map handing "The wallet." to "What did you do while you waited?" as a counting answer. A filler that does not answer its question
is a wrong label, and a wrong label teaches the hollow-present error the tally exists to refuse.
usage: python scripts/synth.py [rows_per_question=200]"""
import json, os, random, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rai.whole import load_whole

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
PER_Q = int(sys.argv[1]) if len(sys.argv) > 1 else 200

# whole/qid -> phrases that answer that question and read after its stem ("It is " + "dark grey"). Lower-case, no full stop.
FILL = {
 "stone/colour": ["dark grey", "brown with black specks", "off-white", "rust red", "grey with a white streak", "greenish grey", "black, shiny where it is wet", "light brown all over"],
 "stone/size": ["about the size of a one-rupee coin", "a little bigger than my thumbnail", "as long as my little finger", "the size of a marble", "as big as a peanut", "about as wide as two fingers"],
 "stone/shape": ["shaped like a flattened egg", "a rough triangle", "round, like a laddoo", "a lump with one flat side", "long and thin like a finger", "a wedge"],
 "stone/feel": ["rough and cold", "smooth on one side, gritty on the other", "smooth all over", "cold and a bit damp", "dusty and dry", "warm from my pocket"],
 "stone/marks": ["a white line across the middle", "a small chip on one corner", "a black spot near the edge", "a crack down one side", "a rusty patch on the flat side", "none"],
 "stone/from": ["the path outside the library", "the riverfront steps", "the college parking lot", "the ground behind the hostel", "the roadside near the temple", "the garden at home"],
 "handful/count": ["fourteen", "nine", "twenty-two", "seven", "thirty-one", "sixteen", "eleven", "twenty"],
 "handful/biggest": ["one about the size of a peanut", "as big as a ten-rupee coin", "a flat one, thumbnail size", "one the size of a grape", "a long one, as long as my little finger"],
 "handful/smallest": ["like a mustard seed", "a grain of rice", "smaller than a peppercorn", "the size of a sesame seed", "a speck, smaller than a lentil"],
 "handful/colours": ["nine grey, four brown, one white", "all grey except two black", "mostly brown, three reddish", "grey and white, about half each", "eight brown, six grey, two black"],
 "handful/odd": ["one is black and shiny, the rest are dull grey", "one is round, the others are broken", "one is twice the size of any other", "one is white, the rest brown", "none, they are all alike"],
 "handful/from": ["the edge of the cricket ground", "the driveway at home", "a construction pile on the road outside", "the railway track side", "the path by the canteen"],
 "coin/value": ["two rupees, it says Bharat and two", "a ten-rupee coin", "one rupee, with the lion", "five rupees", "twenty rupees, the twelve-sided one"],
 "coin/year": ["2019", "2011", "2022", "2007", "none visible, it is too worn", "2015"],
 "coin/sides": ["the lion capital on one side, the number two on the other", "the Ashoka pillar on one side, ten with the rays on the other", "a thumbs-up hand on one side, the lions on the other", "the lions on one side, a five and a wheat stalk on the other"],
 "coin/wear": ["dull, with scratches on the number side", "shiny, almost new", "worn smooth at the rim", "bent a little", "dark, with a green spot"],
 "coin/from": ["change from the tea stall this morning", "the auto driver gave it as change", "my mother's purse", "change at the canteen", "the bus conductor"],
 "coin/now": ["in my left pocket", "on the desk next to the keyboard", "in the pen stand", "in the front pocket of my bag", "on the table by the bed"],
 "leaf/plant": ["a neem tree", "the peepal outside the gate", "tulsi from the pot on the balcony", "a mango tree", "the banyan by the road", "a curry leaf plant"],
 "leaf/size": ["as long as my little finger", "bigger than my palm", "about as wide as two fingers", "the length of my hand", "smaller than my thumb"],
 "leaf/colour": ["green, yellow at the edges", "dark green all over", "brown, with green near the stem", "pale green, darker along the veins", "yellow all over"],
 "leaf/edge": ["toothed like a saw", "smooth", "torn on one side", "wavy", "curled under"],
 "leaf/marks": ["two holes near the tip", "black spots along the vein", "a brown patch at the base", "a bite out of one side", "none"],
 "leaf/where": ["on the footpath under the tree", "still on the branch, I picked it", "on the bonnet of the car", "in the gutter by the gate", "on the steps"],
 "queue/where": ["the canteen counter", "the bank on CG Road", "the bus stop at Paldi", "the railway ticket window", "the photocopy shop"],
 "queue/for": ["tea and a vada pav", "to deposit a cheque", "the 52 bus", "a train ticket", "printouts"],
 "queue/ahead": ["six people", "about fifteen", "two", "nine", "one"],
 "queue/long": ["ten minutes", "half an hour", "three or four minutes", "twenty minutes", "an hour"],
 "queue/front": ["a woman with a red bag", "two students from my class", "an old man with a walking stick", "a man in a blue shirt on his phone", "a girl in school uniform"],
 "queue/did": ["looked at my phone", "counted the tiles on the floor", "talked to the person behind me", "read the notice on the wall", "stood and stared at the fan"],
 "wait/where": ["at the lift on the third floor", "the bus stop outside the campus", "in the car at the railway crossing", "outside the principal's office", "at the chai stall"],
 "wait/for": ["the lift", "the 41 bus", "the train to pass", "my turn at the counter", "the rain to stop"],
 "wait/long": ["four minutes", "about twenty minutes", "nearly an hour", "eight minutes", "half an hour"],
 "wait/looked": ["the floor numbers going up and down", "a hoarding for a jewellery shop", "the gate man's chair", "the crows on the wire", "the notice board"],
 "wait/did": ["held my bag strap", "nothing, they were in my pockets", "scrolled on the phone", "turned the ring on my finger", "held the umbrella"],
 "wait/ended": ["the lift came", "the bus arrived and I got on", "the train passed and the gate opened", "my name was called", "it stopped raining"],
 "tea/water": ["one cup", "two cups", "half a litre", "a cup and a half", "one small pan, about two cups"],
 "tea/tea": ["two spoons of Wagh Bakri", "one teabag of Red Label", "one and a half spoons of loose tea", "a spoon of Society tea", "two teabags of Taj Mahal"],
 "tea/milk": ["half a cup of milk, one spoon of sugar", "no milk, two sugars", "a splash of milk, no sugar", "a cup of milk, no sugar", "no milk, no sugar"],
 "tea/steps": ["boiled the water, added the tea, then the milk, then the sugar, strained it", "water and tea together, boiled twice, milk at the end", "teabag in the cup, poured the water, left it three minutes, added milk", "milk and water together, tea in when it boiled, sugar last"],
 "tea/time": ["seven minutes", "about five minutes", "ten minutes", "four minutes", "twelve minutes"],
 "tea/done": ["it turned dark brown and rose up once", "the colour was right, like the tea stall's", "it boiled over the second time", "it smelt of cardamom", "the froth came up"],
 "walk/ends": ["my flat to the Reliance Fresh on the corner", "the hostel gate to the bus stop", "the office to the chai stall", "home to the milk booth", "the classroom to the canteen"],
 "walk/time": ["six minutes", "about ten minutes", "three minutes", "fifteen minutes", "eight minutes"],
 "walk/pass": ["the temple, the tyre shop, then the school gate", "a paan shop, then the park", "the society gate, the garbage bin, the milk booth", "the bank, then the bakery", "two hostels and the library"],
 "walk/underfoot": ["paver blocks, broken in places", "tar road", "mud and gravel", "concrete, cracked", "sand, then tar"],
 "walk/see": ["the watchman and the milk boy", "nobody, usually", "the same two dogs", "the paan-wala", "the security guard"],
 "walk/instead": ["go round by the main road", "take the auto", "wait till it clears", "cut through the college", "ask somebody to bring it"],
 "pocket/list": ["keys, a pen, the phone, a folded bus ticket", "the phone, the wallet, an earphone case", "a handkerchief, two coins, the ID card", "keys and the phone", "a pen, a receipt, the phone, a lip balm"],
 "pocket/count": ["four things", "three", "five", "two", "six"],
 "pocket/oldest": ["the keys, since I moved in, 2023", "the wallet, three years", "the ID card, since first year", "the pen, since June", "the coin, about a month"],
 "pocket/heaviest": ["the phone", "the keys", "the wallet", "the earphone case", "the bunch of keys"],
 "pocket/miss": ["the keys", "the phone", "the ID card", "the wallet", "the bus pass"],
 "pocket/night": ["on the shelf by the door", "in the drawer", "on the table next to the bed", "in the bag, hung on the chair", "on the fridge"],
 "sound/what": ["the ceiling fan", "a drill from the next building", "crows outside", "the fridge", "a scooter horn", "the water pump"],
 "sound/where": ["above me", "from the left, across the road", "the window behind me", "the corridor", "downstairs"],
 "sound/pattern": ["steady", "it stops and starts", "one-off, every few minutes", "a slow beat", "continuous, with a rattle in it"],
 "sound/loud": ["as loud as a fridge", "louder than the traffic", "quieter than my own typing", "as loud as somebody talking in the next room", "about as loud as the fan"],
 "sound/since": ["I came in this morning", "about ten minutes", "the power came back", "I sat down", "eight o'clock"],
 "sound/stops": ["I switch it off", "they finish the wall", "the sun goes down", "the tank fills", "the bus leaves"],
 "artwork/medium": ["oil on canvas", "watercolour on handmade paper", "acrylic on board", "charcoal on newsprint", "cast bronze", "fired terracotta", "woodcut print on rice paper", "ink and gouache on silk", "carved teak", "embroidered cotton", "oil on jute", "photographic print on fibre paper", "pencil and wash on card", "chalk and charcoal on grey paper", "enamel on tin", "thread on canvas"],
 "artwork/size": ["about 60 by 90 centimetres", "as tall as a door", "small enough to hold in one hand", "120 centimetres across", "about the size of a school notebook", "two metres high and a metre wide", "30 by 40 centimetres", "as long as my arm", "about knee height", "a little bigger than an A4 sheet", "45 centimetres tall on its base", "three panels, each a metre square"],
 "artwork/maker": ["my grandmother", "an unknown painter from Kutch", "a potter in Khurja", "the artist whose name is on the back", "a student at the art school", "a workshop of weavers in Varanasi", "my uncle, who painted signboards", "a printmaker who ran a studio in Baroda", "unknown", "two sisters who worked together", "a temple carver", "a photographer from the local studio", "nobody knows", "not known", "unsigned, so nobody knows", "no record of who made it"],
 "artwork/date": ["1974", "the early 1990s", "2008", "sometime between 1950 and 1960", "1932", "the 1980s", "2016", "around 1900", "1965", "the late 1970s", "2021", "about 1945", "some time in the 2000s", "the middle of the last century", "around the turn of the century", "some time after 1970"],
 "artwork/title": ["Evening at the Ghat", "untitled", "Two Women with a Basket", "Monsoon Study No. 3", "The Blue Door", "Self-portrait with Lamp", "Harvest", "Market, Morning", "Mother and Child", "Study of Hands", "Kite Festival", "Still Life with Brass Pot", "it has no title", "untitled, as far as anyone knows", "no title was ever given", "known only as a study"],
 "artwork/marks": ["a signature in the bottom right corner", "a gallery label on the back of the frame", "an inscription in Devanagari along the lower edge", "none", "a stamp from an exhibition on the stretcher", "initials and a date scratched into the base", "a handwritten number on the back", "a torn price tag on the reverse", "the artist's seal in red ink, top left", "a dedication written across the back", "a customs sticker under the base", "pencil notes along the margin", "nothing at all", "no marks anywhere", "nothing on it", "no signature and no label"],
 "artwork/where": ["in the front room at home", "in storage at the college", "on the wall of the staff room", "in a crate in my garage", "at the district museum, first floor", "in the reading room of the library", "with a framer on Relief Road", "in my sister's flat", "in the office corridor", "in a bank locker", "on loan to a gallery in Mumbai", "in the temple office"],
 "artwork/history": ["in my grandparents' house in Rajkot", "with the dealer who sold it", "nowhere else", "in a private collection in Pune", "in the college auditorium", "with the family of the artist", "in a hotel lobby", "at an exhibition in Delhi", "in my father's shop", "in a school hall", "with a collector in London", "in the old bungalow before it was sold", "it has always been here", "nowhere, it has not moved", "it was made here and stayed", "no earlier place"],
}
# questions of one whole whose answers can legitimately swap: never used as off-question pairs for each other
EXCHANGEABLE = [{"pocket/oldest", "pocket/heaviest", "pocket/miss"}, {"handful/biggest", "handful/smallest"}, {"queue/long", "wait/long", "walk/time", "tea/time"}, {"artwork/where", "artwork/history"}]

EVASIVE = ["It is really nice.", "Hard to say.", "Not sure.", "The usual.", "A lot of things.", "It works well.", "I don't know yet.", "Whatever is there.",
           "Something, I guess.", "Maybe later.", "It is fine.", "Nothing special.", "Depends.", "Can't tell right now.", "All sorts.", "Many.", "It is good.", "You know."]
DEFERRED = ["Not sure yet.", "To be decided.", "Ask me later.", "I'll check.", "Can't tell.", "Let me think.", "I'd have to look."]
GENERAL = ["Everyone in the building.", "Hundreds of them.", "All over the place.", "Loads, really.", "The whole area.", "Everything you can think of.", "Lots and lots."]
EMPTY = ["", "-", "?", "yes", "ok", "hm"]

# Held out: no phrase in the test set may appear in training, in any class. Until 22 September 2026 153 of the test set's
# 180 honest answers were also training fillers, so the reader was scored partly on recall. Refused here, and checked at the end.
norm = lambda t: t.strip().lower().rstrip(".")
HELD = {norm(json.loads(l)["answer"]) for t in ("testset-v1.jsonl", "testset-artwork-v1.jsonl") for l in open(os.path.join(HERE, "tests", t))}
EVASIVE, DEFERRED, GENERAL = ([a for a in L if norm(a) not in HELD] for L in (EVASIVE, DEFERRED, GENERAL))

qs = {}
for path in sorted(glob.glob(os.path.join(HERE, "wholes", "*.yaml"))):
    w = load_whole(path)
    for q in w["questions"]:
        qs[f"{os.path.basename(path)[:-5]}/{q['id']}"] = q
missing = [k for k in qs if k not in FILL]
if missing:
    raise SystemExit(f"no fillers for {missing}; every question needs its own")
# a filler is held out if it, or the stem read out before it (a restating row), is a test answer
FILL = {k: [a for a in v if norm(a) not in HELD and norm(qs[k]["stem"] + a) not in HELD] for k, v in FILL.items() if k in qs}
if not all(FILL.values()):
    raise SystemExit(f"holding out the test set left no fillers for {[k for k, v in FILL.items() if not v]}")


def swappable(a, b):
    return any(a in g and b in g for g in EXCHANGEABLE)


rows = []
for key, q in qs.items():
    f = FILL[key]
    others = [k for k in qs if k.split("/")[0] == key.split("/")[0] and k != key and not swappable(k, key)]
    for _ in range(PER_Q):
        r = random.random()
        if r < 0.40:                                   # bare particular, as people say it
            a = random.choice(f); ans = a[0].upper() + a[1:] + "."
            rows.append(dict(question=q["text"], stem=q["stem"], answer=ans, span=a, cls="bare"))
        elif r < 0.50:                                 # restating particular: the stem read out, then the answer
            a = random.choice(f); ans = q["stem"] + a + "."
            rows.append(dict(question=q["text"], stem="", answer=ans, span=a, cls="restating"))
        elif r < 0.65:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(EVASIVE), span=None, cls="evasive"))
        elif r < 0.75:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(DEFERRED), span=None, cls="deferred"))
        elif r < 0.85:                                 # off-question: a real answer to a different, non-swappable question of the same whole
            o = random.choice(others); a = random.choice(FILL[o]); ans = a[0].upper() + a[1:] + "."
            rows.append(dict(question=q["text"], stem=q["stem"], answer=ans, span=None, cls="off-question"))
        elif r < 0.90:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(EMPTY), span=None, cls="empty"))
        else:
            rows.append(dict(question=q["text"], stem=q["stem"], answer=random.choice(GENERAL), span=None, cls="general"))

leak = [r["answer"] for r in rows if norm(r["answer"]) in HELD or (r["span"] and norm(r["span"]) in HELD)]
if leak:
    raise SystemExit(f"{len(leak)} training rows repeat the test set, e.g. {leak[0]!r}")
random.shuffle(rows)
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
out = os.path.join(HERE, "data", "train-synth.jsonl")
with open(out, "w") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "rows", dict(Counter(r["cls"] for r in rows)), "->", out)
