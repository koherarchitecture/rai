"""0.3.7's new rows: questions as people write them in rai ka pahad, never seen before, answered bare.
rai ka pahad's questions are written live by the two people, so every one is new to the reader and none carries a stem. 0.3.6 learned
116 questions (GRAPEVINE.md, 13u) and misses plain answers to new ones, names most of all (13z8). These rows teach the match between the
kind of thing a question asks for and the kind of thing an answer gives: a person for who, a place for where, a time for when, and so on,
over many questions built from a template and a thing. Every word here was written in Claude Code on 26 September 2026; nothing was
written by Comma. Held out: every test set's answers, rai ka pahad's test questions and things, and the unseen forms' things and questions.
usage: python scripts/synth_live.py [rows]   -> data/train-live.jsonl"""
import glob, json, os, random, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 11600
random.seed(37)

# things the questions are about: ordinary, from an office, a school or a home. None of rai ka pahad's test things (photocopier, tea,
# lift, fan, file, clock) and none of the unseen forms' things or their neighbours (bottle, charger, rain, search, umbrella, glass of
# water, email, website).
THINGS = ["office cooler", "notice board", "stapler", "projector", "AC remote", "store-room key", "attendance register", "school bell",
          "main gate", "bicycle stand", "geyser", "tube light", "wall calendar", "whiteboard", "duster", "steel cupboard", "wooden bench",
          "scooter", "pressure cooker", "gas cylinder", "kitchen tap", "dustbin", "plant pot", "doormat", "mirror", "curtain", "window grill",
          "inverter", "wifi router", "TV remote", "mixer", "bucket", "broom", "bus pass", "tiffin box", "first-aid box", "fire extinguisher",
          "visitors' book", "rubber stamp", "trophy shelf", "cricket bat", "ceiling", "staircase railing", "pen stand", "sewing machine",
          "ladder", "extension board", "raincoat hook", "shoe rack", "overhead tank", "letter box", "name plate", "soap dish", "towel rail"]

WHO = ["Who fixed the {t}?", "Who brought the {t}?", "Who last used the {t}?", "Who is in charge of the {t}?", "Who complained about the {t}?",
       "Who moved the {t}?", "Who put the {t} there?", "Who told you about the {t}?", "Who has the key to the {t}?", "Who cleaned the {t}?",
       "Who else noticed it?", "Who was standing near the {t}?", "Who paid for the {t}?", "Who was it?"]
WHERE = ["Where is the {t} kept?", "Where did you find the {t}?", "Where was the {t} before?", "Where did you put the {t}?",
         "Where does the {t} go at night?", "Where was it bought?", "Where exactly did it happen?", "Where is the {t} now?"]
WHEN = ["When did the {t} break?", "When was the {t} last cleaned?", "When did you notice it?", "When does the {t} get switched on?",
        "When did the {t} arrive?", "What time did it happen?", "When did you last see the {t}?", "Which day was it?"]
COUNT = ["How many people use the {t}?", "How many times did it happen?", "How many of them were there?",
         "How many days did the {t} take to come back?", "How many rupees did the {t} cost?", "How many steps from the door is the {t}?"]
COLOUR = ["What colour is the {t}?", "What colour was it before?", "What colour is the mark on the {t}?"]
MADE = ["What is the {t} made of?", "What was the {t} made of, the old one?"]
OBJECT = ["What was on the {t}?", "What did you use instead of the {t}?", "What was written on the {t}?", "What was kept next to the {t}?",
          "What fell off the {t}?", "Which one was it?"]
LONG = ["How long did it take?", "How long has the {t} been like this?", "How long did you wait for the {t}?", "How long does the {t} last?"]
BRAND = ["What brand is the {t}?", "Which company made the {t}?", "what make is the {t}"]
FOOD = ["What did you have for lunch?", "What was for breakfast?", "What did they serve at the function?", "What was in your tiffin?"]
ABOUT = ["What was the circular about?", "What's the new notice about?", "What was the meeting about?", "What was the message about?"]
# 0.3.7, repaired 27 September 2026: the kinds its first cut missed (a group or a role for who, an errand for where a person is,
# a bare ordinal, a short reason), none of them in any held-out set or in the player input it was checked on.
WHEREABOUTS = ["Where is the {p}?", "Where did the {p} go?", "where's the {p}", "Where is Mitesh?", "where did anjali go", "Where was the {p} this morning?"]
PEOPLE = ["accountant", "driver", "supervisor", "electrician", "librarian", "cook", "watchman", "receptionist", "office boy", "plumber"]
ORDINAL = ["Which floor is the {t} on?", "Which year is he in?", "which bench does she sit on", "Which class is your son in?", "Which lane is it?",
           "which shelf is the {t} on", "Which platform does it leave from?", "which period is it"]
# 0.3.7, 27 September 2026, on "all Indian names should be recognised as names": first names and family names from many languages and
# communities, alone, with a family name, with an initial, with the word people put on them. None of the names probe's
# (/private/tmp probe, recorded in the README) is here.
FIRST = ["Arul", "Kayal", "Senthil", "Mathivanan", "Nandhini", "Selvi", "Priyanka", "Revathi", "Murugan", "Anbu", "Ezhil", "Kaviya",
         "Bijoy", "Lijo", "Remya", "Sajeev", "Nimisha", "Unni", "Deepthi", "Rajeevan", "Anjana", "Soumya", "Harikrishnan", "Gopika",
         "Lokesh", "Sravani", "Bhargav", "Tejaswini", "Ramana", "Sirisha", "Chaitanya", "Vasavi", "Keshav", "Prasanna", "Yashwanth",
         "Nagaraj", "Shwetha", "Girish", "Pavithra", "Umesh", "Rakshitha", "Siddalingappa", "Chaya", "Mahantesh", "Roopa",
         "Sourav", "Ananya", "Joydeep", "Paromita", "Riddhi", "Sayan", "Barnali", "Indrani", "Supriyo", "Tuhin", "Moumita",
         "Bidisha", "Nabajit", "Jahnavi", "Porag", "Lakhimi", "Dhrubajyoti", "Mridul", "Lalnunpuii", "Vanlalruata", "Sangtea", "Ibomcha",
         "Bembem", "Tomba", "Sonam", "Karma", "Tashi", "Yangchen", "Nima", "Lhakpa", "Dechen", "Salkhan", "Budhram", "Sukro", "Mangri",
         "Jaspreet", "Navdeep", "Harleen", "Kuldeep", "Manpreet", "Jasleen", "Gurdeep", "Amrit", "Sukhwinder", "Taranjit",
         "Irfan", "Sameer", "Rehana", "Salma", "Asif", "Farzana", "Junaid", "Nazia", "Yusuf", "Shaheen", "Adil", "Mumtaz", "Arshad",
         "Sabiha", "Tanveer", "Rizwana", "Ayaan", "Inaya", "Kabir", "Zara", "Xavier", "Stella", "Clement", "Roshni", "Wilson", "Agnes",
         "Dominic", "Celine", "Percy", "Zarine", "Jamshed", "Shirin", "Kersi", "Roxana", "Dinshaw", "Hemal", "Parth", "Dhruvi", "Krupa",
         "Nirav", "Foram", "Jayant", "Hiral", "Mitul", "Urvashi", "Ketan", "Snehal", "Rutuja", "Sagar", "Aditi", "Shrikant", "Madhavi",
         "Vaibhav", "Gauri", "Nilesh", "Swapnil", "Ashwini", "Rameshwar", "Sunanda", "Bhola", "Kamla", "Ramdeen", "Sushila", "Jagdish",
         "Phool Singh", "Shanti", "Lallan", "Kallu", "Tinu", "Babli", "Chintu", "Golu", "Monu", "Sweety", "Pintu", "Bunty", "Chiku",
         "Rocky", "Lovely", "Happy", "Sunny", "Bobby", "Rosy", "Jolly", "Ruby", "Daisy", "Lily", "Rose", "Crystal",
         "Arjun", "Meher", "Tara", "Veer", "Ira", "Myra", "Vihaan", "Reyansh", "Aarav", "Diya", "Saanvi", "Pari", "Aadhya", "Mishti"]
FAMILY = ["Pillai", "Menon", "Kurup", "Reddy", "Chowdary", "Gowda", "Hegde", "Shetty", "Banerjee", "Mukherjee", "Das", "Saikia",
          "Gogoi", "Hmar", "Singh", "Sandhu", "Gill", "Khan", "Qureshi", "Ansari", "Siddiqui", "D'Costa", "Pereira", "Mistry", "Irani",
          "Wadia", "Patel", "Joshi", "Desai", "Kulkarni", "Deshpande", "Jadhav", "Pawar", "Yadav", "Mishra", "Tiwari", "Chauhan",
          "Meena", "Munda", "Tudu", "Lepcha", "Sherpa", "Thakur", "Bora", "Kalita", "Nath", "Iyengar", "Nadar", "Thevar", "Ezhava"]
WORDS_ON = ["bhai", "ben", "di", "da", "ji", "garu", "amma", "chettan", "anna", "akka", "tai", "kaka", "paaji", "aapa", "chacha",
            "uncle", "aunty", "sir", "ma'am", "madam", "saab", "bhaiya", "didi", "mausi", "dada", "babu"]


def a_name():
    f = random.choice(FIRST); r = random.random()
    if r < 0.35: n = f
    elif r < 0.6: n = f"{f} {random.choice(FAMILY)}"
    elif r < 0.85: n = f"{f} {random.choice(WORDS_ON)}"
    elif r < 0.93: n = random.choice(FAMILY) + " " + random.choice(["sir", "madam", "ji", "saab", "ma'am"])
    else: n = f"{f[0]}. {random.choice(FAMILY)}"
    return n + "."


# what a verb takes, and what makes a noise or a smell: the kind of meaning 0.3.7 missed (The leave circular. for what was being copied)
DONE = {"printed": ["The transfer circular.", "Report cards for 8B.", "The exam timetable.", "Last year's question paper.", "Visiting cards."],
        "signed": ["The salary sheet.", "My leave form.", "The gate pass register.", "A bonafide certificate.", "The purchase order."],
        "carried": ["Two cartons of registers.", "The sound system.", "A stack of chairs.", "The science models.", "Sacks of rice."],
        "fixed": ["The ceiling fan in room 3.", "A leaking tap.", "The broken hinge.", "The water pump.", "The bell switch."],
        "delivered": ["A parcel for the office.", "Forty water cans.", "The new textbooks.", "A courier from the board.", "Chairs from the dealer."],
        "painted": ["The compound wall.", "The notice board frame.", "The staff room door.", "The flag post.", "The benches in the lab."],
        "sold": ["Old newspapers.", "Scrap iron from the store.", "Raffle tickets.", "The broken benches.", "Last year's uniforms."],
        "cooked": ["Khichdi for everyone.", "Poha and tea.", "Rajma and rice.", "Chole for the function.", "Vegetable pulao."]}
DONE_Q = ["What was being {v}?", "what got {v}", "What did they have {v}?", "What did you see being {v}?"]
SOURCE = {"noise": ["A generator next door.", "Pigeons on the ledge.", "The loose window pane.", "Drilling on the third floor.", "The old cooler."],
          "smell": ["Paint drying in the corridor.", "The drain outside.", "Someone's incense stick.", "Burnt toast in the pantry.", "The new carpet."],
          "leak": ["A crack in the tank.", "The AC pipe.", "The terrace drain.", "A loose joint under the sink."]}
SOURCE_Q = ["What is making the {s}?", "what's causing the {s}", "Where is the {s} coming from?", "What made the {s}?"]
REF = ["Which page was it on?", "Which room is the {t} in?", "Which shelf is the {t} on?", "Which bus goes past the {t}?", "Which number is written on the {t}?"]
WHY = ["Why do you think the {t} broke?", "Why was the {t} moved?", "Why does it happen only sometimes?"]

NAMES = ["Anjali.", "Mr Shah.", "Farhan from the store.", "Meena ben.", "Gurpreet.", "Mrs Iyer.", "Joseph sir.", "Lakshmi, the cleaner.",
         "My neighbour, Vivek.", "Me.", "My brother.", "The driver, Salim.", "Priya from admissions.", "Nandini.", "Arjun and Tanvi.",
         "The watchman, Bahadur.", "Mrs Fernandes.", "Hitesh bhai.", "Our class monitor, Aditi.", "Sister Mary.", "Mr Bhattacharya.",
         "Zoya.", "The plumber, Mahesh.", "My mother.", "Deepak from the second floor.", "Ms Kulkarni.", "Imran.", "Harpreet ma'am.",
         "The principal.", "The new accountant, Neha.", "Babu, the tea boy.", "Kavya.", "Mr Rao from purchase.", "Sunita didi.",
         "My landlord.", "Ali.", "The lab assistant, Prakash.", "Jyoti.", "Chandan and his cousin.", "Mrs D'Souza.", "Ravi.",
         "Pooja from the front desk.", "The electrician from Maninagar.", "Om.", "Fatima.", "Mr Menon.", "Govind.", "Asha.",
         "The sweeper, Raju.", "Tenzin.", "Mr Chauhan, the supervisor.", "Sneha.", "Our driver.", "My colleague Shruti.", "Vikram."]
PLACES = ["Behind the cupboard.", "In the second drawer.", "Near the main gate.", "On the terrace.", "At the bus stop outside the bank.",
          "Under the stairs.", "In the principal's office.", "On top of the fridge.", "By the window in room 12.", "In the store room.",
          "Next to the water tank.", "On the shelf above the sink.", "In the car boot.", "At the hardware shop on CG Road.",
          "In the corner by the door.", "On the third step.", "Outside the canteen.", "In my bag.", "On the balcony.",
          "In the parking, near pillar 4.", "Behind the reception desk.", "In the lab.", "On the roof, by the dish antenna.",
          "Under my desk.", "At Law Garden market.", "In the kitchen, left of the stove.", "In the corridor by the lockers."]
TIMES = ["At 9:15.", "Monday morning.", "Last Thursday.", "On the 3rd.", "Around half past four.", "Just after the lunch break.",
         "On Diwali.", "In June, before the rains.", "Yesterday evening.", "At 7 in the morning.", "Two days ago.", "During the exam week.",
         "On Saturday.", "At midnight.", "Before the assembly.", "Last month, on the 21st.", "In 2019.", "This morning, at 8.",
         "At the end of the second period.", "On Republic Day.", "At 6:30 pm.", "Right after the power cut."]
NUMBERS = ["Three.", "Twelve of them.", "About forty.", "Two.", "Seven times.", "Just one.", "Eighteen.", "Five hundred rupees.",
           "Nine days.", "Around thirty people.", "Four.", "Twenty-two steps.", "A hundred and fifty rupees.", "Six.", "Eleven."]
COLOURS = ["Pale yellow.", "Navy blue with white stripes.", "Grey.", "A dull green.", "Bright orange.", "White, gone brown at the edges.",
           "Maroon.", "Sky blue.", "Black with a red handle.", "Off-white.", "Silver.", "Pink, faded.", "Dark brown.", "Purple."]
MATERIALS = ["Steel.", "Plastic.", "Teak wood.", "Aluminium.", "Cast iron.", "Cardboard.", "Glass.", "Bamboo.", "Stainless steel and rubber.",
             "Cotton cloth.", "Brass.", "Plywood with a sunmica top.", "Clay.", "Jute."]
OBJECTS = ["A stack of old newspapers.", "The blue register.", "A bunch of keys.", "An old Nokia phone.", "A plastic chair.",
           "A torch.", "Chalk and a duster.", "The fee receipt book.", "A calendar from 2022.", "A spare bulb.", "A roll of tape.",
           "A steel glass.", "The class photograph.", "A broken padlock.", "My ID card.", "A packet of pencils.", "A pair of scissors.",
           "The sign-in sheet.", "A tin of paint.", "A rolled-up mat."]
DURATIONS = ["Ten minutes.", "Two hours.", "Three weeks.", "Half a day.", "About twenty minutes.", "Since March.", "Forty-five minutes.",
             "A whole month.", "Five minutes.", "Since the monsoon.", "An hour and a half.", "Eight months."]
REFS = ["Page 9.", "Page 42.", "Room 204.", "The fourth shelf.", "Number 36.", "Bus 51.", "Chapter 3.", "Row 5.", "Platform 2.", "Locker 118."]
BRANDS = ["Godrej.", "Usha.", "Havells.", "Bajaj.", "Prestige.", "Philips.", "Crompton.", "Hero.", "Camlin.", "Milton.", "Nilkamal.", "Syska."]
FOODS = ["Poha.", "Rajma chawal.", "Idli and chutney.", "Veg biryani.", "Chole kulche.", "Upma.", "Masala dosa.", "Vada pav.",
         "Khakhra and pickle.", "Sprouts salad.", "Dal dhokli.", "Undhiyu and puri."]
ABOUTS = ["Exam dates changed.", "The new dress code.", "Holiday on Friday.", "Fee hike from next term.", "Parking only on the left side.",
          "Biometric attendance from Monday.", "The annual day rehearsal.", "Water will be off on Sunday."]
# 0.3.7, for people's typing: names with the words people put on them, digits, short times and dates. None of the player test set's.
NAMES += ["Sharma ji.", "Anu di.", "Ketan bhai.", "Desai sir.", "Rupa ma'am.", "Patel uncle.", "Jignesh.", "Hema aunty.", "Kaka.",
          "The new guy, Yash.", "Mansi di.", "Pandya sir.", "Bhatt madam.", "Lalit bhai."]
TIMES += ["11:30.", "9 am.", "Feb 3.", "12th.", "5:45.", "10 pm.", "Aug 28.", "2.15.", "Mon.", "Sat afternoon."]
NUMBERS += ["8.", "15.", "27.", "4.", "40.", "112.", "9.", "3 of them.", "Like 20.", "300 rupees.", "Rs 50."]
PLACES += ["In the staffroom.", "Near the lab.", "Upstairs, room 9.", "With the peon.", "At the security cabin.", "In the admin block.", "Accounts."]
DURATIONS += ["15 mins.", "2 hrs.", "3 days.", "Half an hour min."]
ERRANDS = ["Gone to the post office.", "Out for chai.", "On leave, at her village.", "Went home early.", "Out on a delivery.",
           "Gone to get change.", "In the washroom.", "At a wedding in Surat.", "Stuck in traffic on the highway.", "Out with the inspection team.",
           "Gone to the other campus.", "At the dentist.", "Waiting at the gate for a parcel.", "Gone to buy stamps."]
ORDINALS = ["3rd.", "1st.", "The 5th.", "Second.", "Ground.", "The top one.", "8th.", "10th.", "The last one.", "6th.", "The first one.", "Fourth."]
NAMES += ["The watchman.", "The class teacher.", "Our supervisor.", "The canteen man.", "The librarian.", "The accountant.", "The cleaner.",
          "The receptionist.", "The cook.", "The security guard.", "Their coach.", "My uncle.", "The vice principal.", "The office boy.",
          "The class rep.", "The 4th years.", "Class 9B.", "The night staff.", "Both the cleaners.", "The girls' hockey team.",
          "The first-year students.", "The admin people.", "The juniors.", "Section C.", "The morning shift.", "The science department."]
MORE_WHY = ["Why was the meeting cancelled?", "why is the office shut", "Why did the class start late?", "why is the {t} locked"]
MORE_REASONS = ["Pipe burst near the gate.", "The lock is jammed.", "Exams start tomorrow.", "Power was off all night.", "Driver was on leave.",
            "Rain flooded the road.", "The fuse blew.", "Nobody paid the bill.", "Fog on the expressway.", "The ink ran out.",
            "It was sent for repair.", "They changed the timetable.", "The key is with the manager.", "A tyre went flat."]
REASONS = ["Because the window faces west and the sun hits it.", "The wiring is old.", "Nobody switches it off at night.",
           "It was too heavy for the hinge.", "Water gets in when it rains.", "The screw was loose from the start.",
           "The children lean on it.", "It was put back in the wrong place.", "The voltage drops in the evening.",
           "The new one is a cheaper make."]

KINDS = {"who": (WHO, NAMES), "where": (WHERE, PLACES), "when": (WHEN, TIMES), "count": (COUNT, NUMBERS), "colour": (COLOUR, COLOURS),
         "made": (MADE, MATERIALS), "object": (OBJECT, OBJECTS), "long": (LONG, DURATIONS), "why": (WHY + MORE_WHY, REASONS + MORE_REASONS), "brand": (BRAND, BRANDS), "food": (FOOD, FOODS), "about": (ABOUT, ABOUTS), "whereabouts": (WHEREABOUTS, ERRANDS + PLACES[:12]), "ordinal": (ORDINAL, ORDINALS), "ref": ([], REFS)}   # ref: labels (Page 9, Bus 51) are only ever wrong answers here; asked as a question of their own they taught that any label answers a which (try 2, Speed 3 for a chair)
# an off-question answer must be of a kind that plainly does not answer: never a kind that could (a duration for a when, an object for a who)
WRONG = {"who": ["where", "when", "count", "colour", "made", "long", "ref"], "where": ["who", "when", "count", "colour", "long"],
         "when": ["who", "where", "colour", "made", "object", "count", "ref"], "count": ["who", "where", "colour", "made", "object"],
         "colour": ["who", "when", "count", "long", "where", "ref"], "made": ["who", "when", "count", "long"],
         "object": ["when", "count", "long", "colour"], "long": ["who", "where", "colour", "made", "object", "ref"],
         "why": ["who", "count", "colour", "when", "ref"],
         "ref": ["who", "when", "colour", "made", "long"], "brand": ["who", "when", "count", "long", "where"],
         "food": ["who", "when", "count", "where", "colour"], "about": ["who", "count", "colour", "made", "where"],
         "whereabouts": ["who", "count", "colour", "made", "brand", "when"], "ordinal": ["who", "when", "long", "made", "about", "food", "ref"],
         "done": ["who", "when", "count", "colour", "long"], "source": ["who", "when", "count", "colour", "ordinal"],
         "name": ["where", "when", "count", "colour", "made", "long", "ref"]}

EVASIVE = ["It is really nice.", "Hard to say.", "The usual.", "It works well.", "Whatever is there.", "It's fine, I suppose.",
           "You know how it is.", "Same as always.", "Depends on the day."]
DEFERRED = ["Not sure yet.", "To be decided.", "Ask me later.", "I'll check.", "Can't tell.", "I'd have to look.", "No idea, honestly.",
            "Probably the usual time.", "I think so.", "Let me ask and tell you."]
GENERAL = ["Everyone in the office.", "Lots of people.", "All over the place.", "Loads, really.", "Somewhere around here.",
           "Whoever was around.", "Sometime back.", "Someone from the other side.", "For a while now.", "Ages, really.",
           "Many times.", "Anybody who needs it.", "Various things."]
EMPTY = ["", "-", "?", "yes", "ok", "hm"]

norm = lambda t: t.strip().lower().rstrip(".")
qnorm = lambda t: t.strip().lower().rstrip("?")
tests = [json.loads(l) for p in glob.glob(os.path.join(HERE, "tests", "testset*.jsonl")) for l in open(p)]
HELD = {norm(r["answer"]) for r in tests}
HELD_Q = {qnorm(r["question"]) for r in tests if r.get("whole") in {"photocopier", "tea", "lift", "fan", "file", "clock", "typing"}}
sys.path.insert(0, HERE)
from rai.whole import load_whole
HELD_Q |= {qnorm(q["text"]) for p in glob.glob(os.path.join(HERE, "tests", "unseen-forms", "*.yaml")) for q in load_whole(p)["questions"]}
HELD_THINGS = {"photocopier", "tea", "lift", "fan", "file", "clock", "bottle", "charger", "rain", "search", "umbrella", "water", "email", "website"}
if any(w in HELD_THINGS for t in THINGS for w in t.lower().replace("-", " ").split()):
    raise SystemExit(f"a thing names a held-out thing: {[t for t in THINGS if any(w in HELD_THINGS for w in t.lower().replace('-', ' ').split())]}")
dropped = [a for _, p in KINDS.values() for a in p if norm(a) in HELD] + [a for p in (EVASIVE, DEFERRED, GENERAL) for a in p if norm(a) in HELD]
KINDS = {k: (qs, [a for a in p if norm(a) not in HELD]) for k, (qs, p) in KINDS.items()}   # a test answer is never trained on, in any class
EVASIVE, DEFERRED, GENERAL = ([a for a in p if norm(a) not in HELD] for p in (EVASIVE, DEFERRED, GENERAL))
print("held out, being test answers:", dropped)


def question(kind):
    if kind == "done":
        v = random.choice(list(DONE)); return random.choice(DONE_Q).format(v=v), random.choice(DONE[v])
    if kind == "source":
        k = random.choice(list(SOURCE)); return random.choice(SOURCE_Q).format(s=k), random.choice(SOURCE[k])
    if kind == "name":
        return random.choice(WHO).format(t=random.choice(THINGS)), a_name()
    q = random.choice(KINDS[kind][0])
    return q.format(t=random.choice(THINGS), p=random.choice(PEOPLE)), random.choice(KINDS[kind][1])


# how people type an answer round the thing itself: the span stays the thing
WRAP_KIND = {"who": ["{x} has it", "{x} did it", "{x} only", "{x}, as usual", "ya {x}"], "where": ["its {x}", "{x} only", "ya {x}", "kept {x}"],
             "count": ["like {x}", "{x} only", "around {x}"], "when": ["{x} only", "ya {x}"]}   # how people type round the thing; the span stays the thing


rows = []
while len(rows) < N:
    kind = random.choice([k for k in KINDS if KINDS[k][0]] + ["done", "source", "name", "name"])   # names twice: "all Indian names should be recognised as names"
    q, a = question(kind)
    if qnorm(q) in HELD_Q or norm(a) in HELD:
        continue
    r = random.random()
    if r >= 0.45 and random.random() < 0.5:        # non-answers typed the same way, so lowercase is never itself a cue
        q = q.lower().rstrip("?")
    if r < 0.45:                                   # bare particular, as people say it
        span = a.rstrip(".")
        if random.random() < 0.5:                  # half typed the way people type
            q = q.lower().rstrip("?"); span = span[0].lower() + span[1:] if kind not in ("who", "name", "brand") or random.random() < 0.6 else span
            w = random.choice(WRAP_KIND.get("who" if kind == "name" else kind, ["{x}", "{x}", "{x} only", "ya {x}"])) if random.random() < 0.3 else "{x}"
            a = w.replace("{x}", span, 1).replace("{x}", span)
        rows.append(dict(question=q, stem="", answer=a, span=span, cls="bare"))
    elif r < 0.60:
        a = random.choice(EVASIVE); rows.append(dict(question=q, stem="", answer=a if q[0].isupper() else a.lower().rstrip("."), span=None, cls="evasive"))
    elif r < 0.70:
        a = random.choice(DEFERRED); rows.append(dict(question=q, stem="", answer=a if q[0].isupper() else a.lower().rstrip("."), span=None, cls="deferred"))
    elif r < 0.85:                                 # off-question: a real answer of a kind that does not answer this question
        wrong = "ref" if kind in ("when", "ordinal") and random.random() < 0.5 else random.choice(WRONG[kind])   # a label (Page 9, Room 204) is not a time or an ordinal: the bare ordinals taught that any number answers a when (Page 17, 27 Sep)
        a = random.choice(KINDS[wrong][1]); rows.append(dict(question=q, stem="", answer=a if q[0].isupper() else a.lower().rstrip("."), span=None, cls="off-question"))
    elif r < 0.90:
        rows.append(dict(question=q, stem="", answer=random.choice(EMPTY), span=None, cls="empty"))
    else:
        a = random.choice(GENERAL); rows.append(dict(question=q, stem="", answer=a if q[0].isupper() else a.lower().rstrip("."), span=None, cls="general"))

out = os.path.join(HERE, "data", "train-live.jsonl")
with open(out, "w") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
from collections import Counter
print(len(rows), "rows,", len({r["question"] for r in rows}), "distinct questions", dict(Counter(r["cls"] for r in rows)), "->", out)
