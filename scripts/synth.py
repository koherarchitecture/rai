"""100% synthetic training pairs, labels by construction. Writes data/train-synth.jsonl.
Row: question, stem, answer, span (the phrase that answers, or null), class. Templates only, seeded; every particular is a plain real thing.
Rewritten 22 September 2026: fillers are written PER QUESTION and phrased to follow that question's stem, after ten sampled rows showed
a keyword map handing "The wallet." to "What did you do while you waited?" as a counting answer. A filler that does not answer its question
is a wrong label, and a wrong label teaches the hollow-present error the tally exists to refuse.
0.3.5, 23 September 2026: eight more forms; three rows in ten read without their stem; every tests/testset*.jsonl is held out; and no
training question may repeat a question from tests/unseen-forms/, which the reader never sees.
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
 "stone/shape": ["a flat oval", "a rough triangle", "round, like a laddoo", "a lump with one flat side", "long and thin like a finger", "a wedge"],
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
 "tea/soymilk": ["half a cup of soy milk, one spoon of sugar", "none, two sugars", "a splash of soy milk, no sugar", "a cup of soy milk, no sugar", "none of either"],
 "tea/steps": ["boiled the water, added the tea, then the soy milk, then the sugar, strained it", "water and tea together, boiled twice, soy milk at the end", "teabag in the cup, poured the water, left it three minutes, added soy milk", "soy milk and water together, tea in when it boiled, sugar last"],
 "tea/time": ["seven minutes", "about five minutes", "ten minutes", "four minutes", "twelve minutes"],
 "tea/done": ["it turned dark brown and rose up once", "the colour was right, like the tea stall's", "it boiled over the second time", "it smelt of cardamom", "the froth came up"],
 "walk/ends": ["my flat to the Reliance Fresh on the corner", "the hostel gate to the bus stop", "the office to the chai stall", "home to the vegetable market", "the classroom to the canteen"],
 "walk/time": ["six minutes", "about ten minutes", "three minutes", "fifteen minutes", "eight minutes"],
 "walk/pass": ["the temple, the tyre shop, then the school gate", "a paan shop, then the park", "the society gate, the garbage bin, the vegetable cart", "the bank, then the bakery", "two hostels and the library"],
 "walk/underfoot": ["paver blocks, broken in places", "tar road", "mud and gravel", "concrete, cracked", "sand, then tar"],
 "walk/see": ["the watchman and the newspaper boy", "nobody, usually", "the same two dogs", "the paan-wala", "the security guard"],
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
 "artwork/medium": ["oil on canvas", "watercolour on handmade paper", "acrylic on board", "charcoal on newsprint", "cast bronze", "fired terracotta", "woodcut print on rice paper", "ink on paper", "carved teak", "embroidered cotton", "oil on jute", "photographic print on fibre paper", "pencil and wash on card", "chalk and charcoal on grey paper", "enamel on tin", "thread on canvas"],
 "artwork/size": ["about 60 by 90 centimetres", "as tall as a door", "small enough to hold in one hand", "120 centimetres across", "about the size of a school notebook", "two metres high and a metre wide", "30 by 40 centimetres", "as long as my arm", "about knee height", "a little bigger than an A4 sheet", "45 centimetres tall on its base", "three panels, each a metre square"],
 "artwork/maker": ["my grandmother", "an unknown painter from Kutch", "a potter in Khurja", "the artist whose name is on the back", "a student at the art school", "a workshop of weavers in Varanasi", "my uncle, who painted signboards", "a printmaker who ran a studio in Baroda", "unknown", "two sisters who worked together", "a temple carver", "a photographer from the local studio", "nobody knows", "not known", "unsigned, so nobody knows", "no record of who made it"],
 "artwork/date": ["1974", "the early 1990s", "2008", "sometime between 1950 and 1960", "1932", "the 1980s", "2016", "around 1900", "1965", "the late 1970s", "2021", "about 1945", "some time in the 2000s", "the middle of the last century", "around the turn of the century", "some time after 1970"],
 "artwork/title": ["Evening at the Ghat", "untitled", "Two Women with a Basket", "Monsoon Study No. 3", "The Blue Door", "Self-portrait with Lamp", "Harvest", "Market, Morning", "Mother and Child", "Study of Hands", "Kite Festival", "Still Life with Brass Pot", "it has no title", "untitled, as far as anyone knows", "no title was ever given", "known only as a study"],
 "artwork/marks": ["a signature in the bottom right corner", "a gallery label on the back of the frame", "an inscription in Devanagari along the lower edge", "none", "a stamp from an exhibition on the stretcher", "initials and a date scratched into the base", "a handwritten number on the back", "a torn price tag on the reverse", "the artist's seal in red ink, top left", "a dedication written across the back", "a customs sticker under the base", "pencil notes along the margin", "nothing at all", "no marks anywhere", "nothing on it", "no signature and no label"],
 "artwork/where": ["in the front room at home", "in storage at the college", "on the wall of the staff room", "in a crate in my garage", "at the district museum, first floor", "in the reading room of the library", "with a framer on Relief Road", "in my sister's flat", "in the office corridor", "in a bank locker", "on loan to a gallery in Mumbai", "in the temple office"],
 "artwork/history": ["in my grandparents' house in Rajkot", "with the dealer who sold it", "nowhere else", "in a private collection in Pune", "in the college auditorium", "with the family of the artist", "in a hotel lobby", "at an exhibition in Delhi", "in my father's shop", "in a school hall", "with a collector in London", "in the old bungalow before it was sold", "it has always been here", "nowhere, it has not moved", "it was made here and stayed", "no earlier place"],
 # 0.3.5: eight more forms, so the reader meets more kinds of question
 "call/who": ["my mother", "the gas agency", "my cousin in Surat", "the plumber", "a friend from school", "the bank's helpline", "my landlord", "the tiffin service", "the courier office", "my brother"],
 "call/about": ["the gas cylinder booking", "a leaking tap in the bathroom", "the rent for this month", "a parcel that had not come", "plans for Sunday", "a blocked debit card", "the date of the exam", "the electricity bill", "picking up my sister from the station", "a lost charger"],
 "call/rang": ["twice", "three times", "once", "five times", "about six times", "only once", "four times", "seven times"],
 "call/first": ["hello, who is this", "haan, bolo", "one minute, I am driving", "good morning, how can I help you", "I was just about to call you", "wrong number", "can I call you back", "yes, tell me"],
 "call/long": ["two minutes", "about ten minutes", "half a minute", "twenty minutes", "an hour", "five minutes", "under a minute", "a quarter of an hour"],
 "call/ended": ["she said she had to go", "the network dropped", "I said I would call back", "they gave me a complaint number", "my battery died", "someone rang the doorbell", "he hung up without saying bye", "we fixed a time for Sunday"],
 "repair/what": ["the zip on my bag", "a dripping tap", "the ceiling fan's regulator", "a loose chair leg", "my phone's charging port", "the bathroom door latch", "a torn slipper strap", "the table lamp", "my earphone cable", "a wobbly shelf"],
 "repair/wrong": ["the washer had worn out", "a screw had fallen out", "the teeth of the zip had come apart", "dust in the port", "a loose wire inside the switch", "the strap had torn at the stitching", "a cracked bulb holder", "one leg was shorter than the others", "the latch did not reach the hole"],
 "repair/used": ["a screwdriver from the kitchen drawer", "a safety pin", "Fevikwik", "cello tape", "a toothpick", "a spanner borrowed from the watchman", "pliers", "a needle and black thread", "an old toothbrush", "a blunt kitchen knife"],
 "repair/first": ["switched off the mains", "turned off the valve under the sink", "took the cover off", "pulled out the plug", "cleaned the port with a toothpick", "unscrewed the base", "looked it up on YouTube", "emptied the bag", "turned the chair upside down"],
 "repair/long": ["ten minutes", "about an hour", "the whole afternoon", "five minutes", "two days, on and off", "twenty minutes", "half an hour", "less than a minute"],
 "repair/worked": ["it held", "the tap still dripped, but slower", "the fan ran again", "it broke again the next day", "the zip closed but the pull came off", "the lamp flickered and then stayed on", "the chair still wobbled", "it worked for a week, then stopped"],
 "lost/what": ["my house keys", "a black umbrella", "my ID card", "one earring", "the TV remote", "my spectacles", "a pen drive with my files", "the gas connection book", "my bus pass"],
 "lost/last": ["on the auto ride home", "at the canteen table", "in my jeans pocket", "on the sofa", "at my desk in the studio", "in the lift", "at the photocopy shop", "on the bus"],
 "lost/checked": ["my bag", "under the bed", "the kitchen counter", "the pockets of yesterday's jeans", "the car", "the drawer by the door", "the bathroom", "the shoe rack"],
 "lost/found": ["inside the pillow cover", "under the car seat", "in my other bag", "on top of the washing machine", "at the lost-and-found desk at the office", "in my brother's room", "behind the sofa cushion", "in the pocket of my raincoat"],
 "lost/time": ["twenty minutes", "two days", "about an hour", "five minutes", "the whole morning", "a week, on and off", "ten minutes", "half an hour"],
 "lost/who": ["me", "my mother", "the watchman", "the auto driver, who brought it back", "my roommate", "the cleaner at the office", "my little sister", "a stranger on the bus"],
 "ride/ends": ["the station to home", "college to the hospital", "Paldi to the airport", "the bus stand to my aunt's place", "the office to the mall", "home to the exam centre", "the market to the hostel", "the metro station to work"],
 "ride/got": ["on the Ola app", "by waving one down on the road", "through Rapido", "on Uber", "from the prepaid auto booth", "by calling a driver I know", "from the stand outside the station", "on the Namma Yatri app"],
 "ride/cost": ["eighty rupees", "a hundred and forty-three rupees", "two hundred and ten rupees", "sixty rupees", "a hundred rupees, and he had no change", "three hundred and twenty-five rupees with the airport charge", "forty rupees", "ninety-five rupees"],
 "ride/time": ["twelve minutes", "about forty minutes", "twenty-five minutes", "an hour in the traffic", "eight minutes", "half an hour", "fifteen minutes"],
 "ride/route": ["by the ring road", "through the old city", "over the Nehru bridge", "the long way, round the lake", "straight down the main road", "over the flyover", "through the back lanes", "past the stadium"],
 "ride/happened": ["we stopped for petrol", "it started raining", "the driver took a call", "we got stuck behind a procession", "a tyre went flat", "the meter stopped working", "the driver asked me the way twice", "we waited at a railway crossing"],
 "message/to": ["my sister", "the class group", "my landlord", "a friend from school", "my father", "the delivery man", "my manager", "the society's WhatsApp group"],
 "message/app": ["WhatsApp", "Signal", "plain SMS", "Telegram", "email", "Google Messages", "Slack", "the college portal"],
 "message/about": ["the time we were meeting", "a photo of the broken tap", "the rent", "notes from the lecture", "a birthday", "the address of the shop", "whether the bus was running", "the OTP I had been sent"],
 "message/length": ["one line", "three words", "just a thumbs-up", "a voice note of forty seconds", "two paragraphs", "a photo and one word", "a single emoji", "about five lines"],
 "message/reply": ["in a minute", "the next morning", "after an hour", "straight away", "two days later", "while I was typing the next one", "at midnight", "after lunch"],
 "message/after": ["put the phone down", "went back to cooking", "sent a second message", "locked the screen", "went to sleep", "checked if it was delivered", "called them instead", "went out"],
 "paperwork/which": ["the leave application at college", "a KYC form at the bank", "the gas connection transfer form", "a courier booking slip", "the library membership form", "an address change form for my Aadhaar", "the hostel room request", "a cheque deposit slip"],
 "paperwork/where": ["at the bank counter", "on the college website", "on my phone, in the app", "at the post office", "at home, then took it in", "standing at the courier desk", "in the office corridor", "on a computer at a cyber cafe"],
 "paperwork/box": ["the one for my father's occupation", "permanent address", "the nominee details", "the reason for leave", "the customer ID", "the date of birth, in the right format", "the signature box, it was tiny", "the PIN code of my village"],
 "paperwork/attached": ["a photocopy of my Aadhaar", "two passport photos", "nothing", "my fee receipt", "a cancelled cheque", "the old connection book", "a self-attested address proof", "my ID card, front and back"],
 "paperwork/long": ["ten minutes", "about half an hour", "two visits", "five minutes", "an hour, with the queue", "twenty minutes", "fifteen minutes", "three days, because of the stamp"],
 "paperwork/after": ["they gave me a token number", "it was stamped and I got a copy", "I got an SMS with a reference number", "they said to come back on Monday", "it came back for a missing signature", "the clerk put it in a tray", "I got an email the same evening", "they asked for one more photocopy"],
 "door/material": ["plywood painted white", "teak", "steel", "glass in an aluminium frame", "pressed board with a laminate", "old wood, painted green many times", "PVC", "sheesham wood"],
 "door/colour": ["off-white", "dark brown", "sky blue", "white, grey near the handle", "grey", "the same colour as the wall", "maroon", "bare wood, unpainted"],
 "door/lock": ["a bolt at the top", "a key, from outside only", "a latch and a padlock", "a round knob with a button", "a tower bolt at the bottom", "nothing, it does not lock", "a chain", "a sliding latch"],
 "door/stuck": ["a calendar from the chemist", "nothing", "a towel on a hook", "a Ganesh sticker", "my timetable", "a small mirror", "two hooks with bags", "a name plate"],
 "door/sound": ["a long creak", "no sound at all", "a click from the latch", "a scrape on the floor", "a squeak at the hinge", "a bang when the fan is on", "a rattle from the loose handle", "a thud against the wall"],
 "door/behind": ["the dustbin", "a stack of old newspapers", "the switchboard", "my bicycle", "the mop and bucket", "just the wall", "a cupboard", "my shoes"],
 "screen/count": ["twelve", "twenty", "eight", "sixteen", "only four", "twenty-four", "nine", "about fifteen"],
 "screen/corner": ["the Phone app", "Google Pay", "the camera", "the clock", "WhatsApp", "PhonePe", "the calendar", "Chrome"],
 "screen/wallpaper": ["a photo of my niece", "the default blue one", "a picture of the sea", "plain black", "a Madhubani painting", "my dog, asleep", "a mountain at sunrise", "plain grey"],
 "screen/most": ["WhatsApp", "YouTube", "the camera", "Google Maps", "the calculator", "Spotify", "the bank app", "Chrome"],
 "screen/never": ["the Files app", "Samsung Health", "the compass", "the FM radio", "Google Pay", "the voice recorder", "the weather app", "the phone's own browser"],
 "screen/dock": ["the phone, messages and camera", "Chrome and WhatsApp", "only the dialer", "the camera, the gallery and Maps", "the phone and the browser", "WhatsApp, YouTube and the camera", "Phone, Messages, Chrome and Camera", "no apps, the bar is empty"],
}
# questions of one whole whose answers can legitimately swap: never used as off-question pairs for each other
EXCHANGEABLE = [{"pocket/oldest", "pocket/heaviest", "pocket/miss"}, {"handful/biggest", "handful/smallest"}, {"queue/long", "wait/long", "walk/time", "tea/time"}, {"artwork/where", "artwork/history"},
                {"call/about", "call/who"}, {"call/ended", "call/first"}, {"repair/worked", "repair/wrong"}, {"repair/first", "repair/used"}, {"lost/checked", "lost/found", "lost/last"}, {"ride/ends", "ride/route"}, {"door/colour", "door/material"}, {"door/behind", "door/stuck"}, {"screen/corner", "screen/dock", "screen/most", "screen/never"}]

EVASIVE = ["It is really nice.", "Hard to say.", "Not sure.", "The usual.", "A lot of things.", "It works well.", "I don't know yet.", "Whatever is there.",
           "Something, I guess.", "Maybe later.", "It is fine.", "Nothing special.", "Depends.", "Can't tell right now.", "All sorts.", "Many.", "It is good.", "You know."]
DEFERRED = ["Not sure yet.", "To be decided.", "Ask me later.", "I'll check.", "Can't tell.", "Let me think.", "I'd have to look."]
GENERAL = ["Everyone in the building.", "Hundreds of them.", "All over the place.", "Loads, really.", "The whole area.", "Everything you can think of.", "Lots and lots."]
EMPTY = ["", "-", "?", "yes", "ok", "hm"]

# Held out: no phrase in the test set may appear in training, in any class. Until 22 September 2026 153 of the test set's
# 180 honest answers were also training fillers, so the reader was scored partly on recall. Refused here, and checked at the end.
norm = lambda t: t.strip().lower().rstrip(".")
HELD = {norm(json.loads(l)["answer"]) for t in glob.glob(os.path.join(HERE, "tests", "testset*.jsonl")) for l in open(t)}   # every test set, the unseen-forms one included
EVASIVE, DEFERRED, GENERAL = ([a for a in L if norm(a) not in HELD] for L in (EVASIVE, DEFERRED, GENERAL))

qs = {}
for path in sorted(glob.glob(os.path.join(HERE, "wholes", "*.yaml"))):
    w = load_whole(path)
    for q in w["questions"]:
        qs[f"{os.path.basename(path)[:-5]}/{q['id']}"] = q
# 0.3.5: the forms in tests/unseen-forms/ are never trained on, so a reader can be measured on questions it has not seen
qnorm = lambda t: t.strip().lower().rstrip("?")
unseen = {qnorm(q["text"]) for p in glob.glob(os.path.join(HERE, "tests", "unseen-forms", "*.yaml")) for q in load_whole(p)["questions"]}
if any(qnorm(q["text"]) in unseen for q in qs.values()):
    raise SystemExit(f"a training question repeats an unseen form's question: {[k for k, q in qs.items() if qnorm(q['text']) in unseen]}")
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

# 0.3.5: forms people write often carry no stem, so three rows in ten are read without one, in every class alike, so a missing stem is never itself a cue
for r in rows:
    if r["stem"] and random.random() < 0.3:
        r["stem"] = ""

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
