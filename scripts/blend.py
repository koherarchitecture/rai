"""Average two readers' weights: out = (1 - share) * first + share * second (0.3.8, 29 September 2026).
0.3.8 is 0.3.7 blended with the reader distilled from the Hinglish teacher, 0.6 of the second: distillation alone read Hinglish twice as
well and Indian names a quarter worse, and the blend keeps most of both. Both start from deepset's MiniLM, so their average is itself a
reader (WiSE-FT and model soups, Wortsman et al. 2022).
usage: python scripts/blend.py <first> <second> <share of second> <out>"""
import sys
from transformers import AutoModelForQuestionAnswering, AutoTokenizer

first, second, share, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
a, b = AutoModelForQuestionAnswering.from_pretrained(first), AutoModelForQuestionAnswering.from_pretrained(second)
sa, sb = a.state_dict(), b.state_dict()
a.load_state_dict({k: (1 - share) * sa[k].float() + share * sb[k].float() for k in sa})
a.save_pretrained(out); AutoTokenizer.from_pretrained(first).save_pretrained(out)
print(f"{out}: {1 - share:.2f} of {first}, {share:.2f} of {second}")
