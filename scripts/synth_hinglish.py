"""0.3.8's new rows: answers in Hinglish, to questions in English and in Hinglish, typed as people type them.
0.3.7 counted 16 of 56 honest Hinglish answers and counted four vague ones (28 September 2026, tests/testset-hinglish-v1.jsonl).
Each row asks about an ordinary thing and answers with a phrase of the kind the question asks for (a person for who, a place for where,
a time for when...), wrapped the way people say it in Hinglish (Ramesh ne kiya, store room mein rakha hai); the span is the phrase.
Every word was written in Claude Code on 28 September 2026. Held out: every test set's answers and questions, and the Hinglish test
set's things (water filter, electricity meter, almirah, stamp pad, doorbell) and rai ka pahad's (photocopier, tea, lift, fan, file, clock).
usage: python scripts/synth_hinglish.py [rows]   -> data/train-hinglish.jsonl"""
import glob, json, os, random, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5800
random.seed(38)

THINGS = ["cooler", "geyser", "inverter", "gas cylinder", "pressure cooker", "scooter", "cycle", "notice board", "projector", "register",
          "tiffin", "TV remote", "wifi router", "mixer", "bucket", "jhadu", "taala", "bench", "whiteboard", "extension board", "tube light",
          "mirror", "darwaza", "khidki", "sofa", "printer", "laptop", "bag", "id card", "attendance sheet", "chabi ka guchha", "gamla"]

NAMES = ["Ramesh", "Suresh", "Pooja", "Neelam", "Imran", "Farida", "Gurpreet", "Joseph", "Lakshmi", "Arjun", "Kavita", "Sunil", "Rekha",
         "Mehul", "Hetal", "Bhavesh", "Anjali", "Salim", "Tenzin", "Priya", "Vikram", "Nirmala", "Dinesh", "Asha", "Rohit", "Shabana",
         "Patel", "Sharma", "Desai", "Iyer", "Khan", "Mehta", "Verma", "Das", "Nair", "Bose"]
HONORIFIC = ["", " ji", " bhai", " bhaiya", " didi", " aunty", " uncle", " sir", " madam", " ben"]
ROLES = ["watchman", "peon", "bijli wala", "plumber bhaiya", "safai wali didi", "chowkidar", "driver bhaiya", "class teacher", "HOD",
         "clerk", "mess wale bhaiya", "padosi", "mama ji", "chachu", "bua", "dadi", "nani", "bhabhi", "office wale bhaiya", "papa", "mummy",
         "chhota bhai", "badi behen", "landlord uncle", "canteen wale", "electrician", "carpenter bhaiya", "kabadi wala", "delivery wala"]
LOCS = ["store room", "rasoi", "balcony", "chhat", "gali", "office", "staff room", "canteen", "seedhi", "parking", "mez", "bistar",
        "fridge", "TV", "khidki", "darwaze", "cupboard", "drawer", "shelf", "godown", "corridor", "lab", "library", "hostel room",
        "bathroom", "aangan", "garage", "dukaan", "bus stand", "auto stand"]
POSTS = ["mein", "pe", "ke paas", "ke upar", "ke neeche", "ke peeche", "ke andar", "ke bagal mein", "ke saamne"]
DAYS = ["somvaar", "mangalvaar", "budhwar", "guruvaar", "shukravaar", "shanivaar", "ravivaar", "Monday", "Friday", "Sunday"]
MONTHS = ["January", "March", "June", "August", "October", "December", "Diwali", "Holi", "Navratri", "exam"]
NUMS = ["ek", "do", "teen", "chaar", "paanch", "chhe", "saat", "aath", "nau", "das", "bees", "pachees", "tees", "pachaas", "sau"]
COLOURS = ["laal", "neela", "neeli", "hara", "hari", "peela", "kaala", "kaali", "safed", "bhura", "gulabi", "narangi", "grey", "silver",
           "aasmani", "jamuni"]
MADE = ["lakdi ka", "steel ka", "plastic ka", "lohe ka", "kaanch ka", "kapde ka", "cement ka", "tin ka", "jute ka", "rubber ka",
        "aluminium ka", "gatte ka", "bamboo ka"]
OBJECTS = ["ek kitaab", "purana calendar", "ek chaabi", "steel ka glass", "do pen", "ek thaila", "akhbaar ka dher", "ek diya",
           "chashma", "ek register", "tulsi ka gamla", "ek tauliya", "chappal", "ek dabba", "rangoli ke colours", "ek chhota Ganesh ji",
           "shaadi ka card", "bijli ka bill", "ek purani ghadi ka band", "rassi"]
SOUNDS = ["khat khat", "tak tak", "ghar ghar", "ting ting", "zor ki awaaz", "seeti jaisi", "gun gun", "khad khad", "dhak dhak",
          "cheen cheen", "bhon bhon", "tap tap"]


def num(): return random.choice(NUMS + [str(random.randint(2, 60))])
def person(): return random.choice([random.choice(NAMES) + random.choice(HONORIFIC), random.choice(ROLES)])
def place(): return f"{random.choice(LOCS)} {random.choice(POSTS)}"
def when():
    return random.choice(["kal", "parso", "aaj subah", "kal raat", "kal shaam", "pichhle hafte", f"{num()} din pehle", f"{random.randint(1, 12)} baje",
                          f"{random.choice(DAYS)} ko", f"subah {random.randint(5, 11)} baje", "shaam ko", "dopahar mein", f"{random.choice(MONTHS)} mein",
                          f"{random.choice(MONTHS)} ke baad", f"{random.choice(DAYS)} subah", f"{num()} hafte pehle", f"pichhle {random.choice(DAYS)}"])
def count(): return f"{num()} {random.choice(['log', 'baar', 'bande', 'bachche', 'dabbe'])}"
def long(): return random.choice([f"{num()} minute", "aadha ghanta", "ek ghanta", "dedh ghanta", f"{num()} ghante", f"{num()} din", "poora din", "poori raat"])
def since(): return f"{num()} {random.choice(['saal', 'mahine', 'hafte', 'din'])} se"
def colour(): return random.choice([random.choice(COLOURS), f"{random.choice(COLOURS)} aur {random.choice(COLOURS)}", f"halka {random.choice(COLOURS)}", f"gehra {random.choice(COLOURS)}"])
def cost(): return random.choice([f"{random.randint(20, 3000)} rupaye", f"{random.choice(NUMS[1:])} sau rupaye", f"{random.randint(20, 900)} ka", "dedh sau", "dhai sau"])

# kind -> (make a phrase, question templates in English and Hinglish, wrappers people put around the phrase)
KINDS = {
 "who": (person, ["Who fixed the {t}?", "Who brought the {t}?", "Who moved the {t}?", "{t} kisne theek kiya?", "{t} kaun laya?", "{t} kisne rakha?", "kaun aaya tha?"],
         ["{x}", "{x} ne", "{x} ne kiya", "{x} laaye the", "{x} aaye the", "{x} ne rakha"]),
 "whohas": (person, ["Who has the {t}?", "{t} kiske paas hai?"], ["{x}", "{x} ke paas", "{x} ke paas hai"]),
 "where": (place, ["Where is the {t} kept?", "Where did you find the {t}?", "{t} kahan rakha hai?", "{t} kahan mila?", "{t} kahan hai?"],
           ["{x}", "{x} hai", "{x} rakha hai", "{x} mila"]),
 "when": (when, ["When did the {t} break?", "When did the {t} come?", "{t} kab kharab hua?", "{t} kab aaya?", "kab hua?"], ["{x}", "{x} hua", "{x} aaya"]),
 "count": (count, ["How many people use the {t}?", "How many times did it happen?", "kitne log use karte hain?", "kitni baar hua?"], ["{x}", "lagbhag {x}", "{x} the"]),
 "long": (long, ["How long did it take?", "How long did the {t} take?", "kitni der lagi?", "{t} mein kitna time laga?"], ["{x}", "{x} lage", "{x} lagi"]),
 "since": (since, ["How long have you had the {t}?", "{t} kab se hai?"], ["{x}", "{x} hai"]),
 "colour": (colour, ["What colour is the {t}?", "{t} kis rang ka hai?"], ["{x}", "{x} hai", "{x} rang ka"]),
 "made": (lambda: random.choice(MADE), ["What is the {t} made of?", "{t} kis cheez ka bana hai?"], ["{x}", "{x} bana hai", "{x} hai"]),
 "cost": (cost, ["How much did the {t} cost?", "{t} kitne ka aaya?"], ["{x}", "{x} ka aaya", "{x} lage"]),
 "object": (lambda: random.choice(OBJECTS), ["What was on the {t}?", "What was kept next to the {t}?", "{t} pe kya rakha tha?", "{t} ke paas kya tha?"],
            ["{x}", "{x} tha", "{x} rakha tha"]),
 "sound": (lambda: random.choice(SOUNDS), ["What sound does the {t} make?", "{t} kaisi awaaz karta hai?"], ["{x}", "{x} karta hai", "{x} awaaz"]),
}
DEFERRED = ["pata nahi", "yaad nahi", "shayad", "maloom nahi yaar", "dekhna padega", "baad mein bataunga", "abhi nahi pata", "pata nai bhai", "yaad nahi aa raha"]
GENERAL = ["koi bhi", "kuch bhi", "sab log", "bahut saare", "kabhi bhi", "kahin bhi", "har jagah", "bahut time se", "kaafi", "jo bhi mila", "kisi ne to kiya hoga"]
EVASIVE = ["theek hai", "achha hai", "normal hai", "wahi purana", "chalta hai", "kya farak padta hai", "haan", "hmm", "chhodo na", "wahi jo hamesha hota hai"]

norm = lambda t: t.strip().lower().rstrip(".?")
tests = [json.loads(l) for t in glob.glob(os.path.join(HERE, "tests", "testset*.jsonl")) for l in open(t)]
HELD, HELD_Q = {norm(r["answer"]) for r in tests}, {norm(r["question"]) for r in tests}
DEFERRED, GENERAL, EVASIVE = ([a for a in L if norm(a) not in HELD] for L in (DEFERRED, GENERAL, EVASIVE))


def typed(text):
    return text if random.random() < 0.5 else text[0].upper() + text[1:] + random.choice(["", "", "."])


rows = []
while len(rows) < N:
    k = random.choice(list(KINDS)); make, questions, wraps = KINDS[k]
    q = random.choice(questions).replace("{t}", random.choice(THINGS))
    q = q[0].upper() + q[1:]
    if norm(q) in HELD_Q: continue
    r = random.random()
    if r < 0.50:
        x = make(); ans = typed(random.choice(wraps).replace("{x}", x)); span, cls = x, "hinglish"
    elif r < 0.65:
        o = random.choice([j for j in KINDS if j != k and {j, k} != {"who", "whohas"} and {j, k} != {"long", "since"}])
        ans, span, cls = typed(KINDS[o][0]()), None, "off-question"
    elif r < 0.75: ans, span, cls = typed(random.choice(DEFERRED)), None, "deferred"
    elif r < 0.87: ans, span, cls = typed(random.choice(GENERAL)), None, "general"
    else: ans, span, cls = typed(random.choice(EVASIVE)), None, "evasive"
    if norm(ans) in HELD or (span and norm(span) in HELD): continue
    if span and span.lower() not in ans.lower(): raise SystemExit(f"span not in answer: {span!r} / {ans!r}")
    rows.append(dict(question=q, stem="", answer=ans, span=span, cls=cls))

out = os.path.join(HERE, "data", "train-hinglish.jsonl")
with open(out, "w") as fh:
    for r in rows: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "rows", dict(Counter(r["cls"] for r in rows)), "->", out)
