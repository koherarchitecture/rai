"""Average the weights of pointed readers made from one base (a uniform model soup, Wortsman et al. 2022) and score the result.
usage: python scripts/soup.py <out-dir> <reader-dir> <reader-dir> ..."""
import sys, subprocess
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
out, srcs = sys.argv[1], sys.argv[2:]
models = [AutoModelForQuestionAnswering.from_pretrained(d) for d in srcs]
sd = {k: sum(m.state_dict()[k].float() for m in models) / len(models) for k in models[0].state_dict()}
models[0].load_state_dict(sd); models[0].save_pretrained(out); AutoTokenizer.from_pretrained(srcs[0]).save_pretrained(out)
subprocess.run([sys.executable, "scripts/eval_reader.py", "tests/testset-v1.jsonl", "tests/testset-artwork-v1.jsonl", "tests/testset-unseen-v1.jsonl", out, "--json", f"{out}/results.json"], check=True, stdout=subprocess.DEVNULL)
