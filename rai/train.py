"""Continue the reader from deepset's weights on rai's synthetic pairs. CPU. Same architecture, nothing added.
usage: python -m rai.train --data data/train-synth.jsonl --out runs/rai-0.3 [--epochs 2] [--rows N] [--lr 2e-5] [--seed 7]
Runs on the GPU when there is one, else CPU; same code, same numbers within float noise."""
import argparse, json, random, time
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from .reader import BASE

ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--base", default=BASE); ap.add_argument("--epochs", type=int, default=2)
ap.add_argument("--rows", type=int, default=0); ap.add_argument("--lr", type=float, default=2e-5); ap.add_argument("--batch", type=int, default=16)
ap.add_argument("--threads", type=int, default=5)
ap.add_argument("--seed", type=int, default=7)  # 0.3.6 is the average of three readers pointed with seeds 7, 1 and 2 (scripts/soup.py)
a = ap.parse_args()
torch.set_num_threads(a.threads); torch.manual_seed(a.seed); random.seed(a.seed)
dev = "cuda" if torch.cuda.is_available() else "cpu"

rows = [json.loads(l) for l in open(a.data)]
if a.rows: rows = rows[:a.rows]
tok = AutoTokenizer.from_pretrained(a.base)
model = AutoModelForQuestionAnswering.from_pretrained(a.base).to(dev)


def features(batch):
    texts = [(r["stem"] + r["answer"]) if r["stem"] and not r["answer"].lower().startswith(r["stem"].strip().lower()) else r["answer"] for r in batch]
    enc = tok([r["question"] for r in batch], texts, truncation="only_second", max_length=384, padding=True, return_offsets_mapping=True, return_tensors="pt")
    starts, ends = [], []
    for i, r in enumerate(batch):
        s = e = 0                                                    # no answer -> [CLS]
        if r["span"]:
            cs = texts[i].lower().find(r["span"].lower()); ce = cs + len(r["span"])
            ids = enc.sequence_ids(i)
            for t, (o0, o1) in enumerate(enc["offset_mapping"][i].tolist()):
                if ids[t] != 1: continue
                if o0 <= cs < o1 and s == 0: s = t
                if o0 < ce <= o1: e = t
            if e < s: s = e = 0
        starts.append(s); ends.append(e)
    del enc["offset_mapping"]
    enc["start_positions"] = torch.tensor(starts); enc["end_positions"] = torch.tensor(ends)
    return enc


opt = torch.optim.AdamW(model.parameters(), lr=a.lr)
loader = DataLoader(rows, batch_size=a.batch, shuffle=True, collate_fn=features)
model.train(); t0 = time.time(); step = 0
for ep in range(a.epochs):
    for batch in loader:
        loss = model(**{k: v.to(dev) for k, v in batch.items()}).loss
        loss.backward(); opt.step(); opt.zero_grad(); step += 1
        if step % 50 == 0: print(f"epoch {ep+1} step {step} loss {loss.item():.3f} {time.time()-t0:.0f}s", flush=True)
model.save_pretrained(a.out); tok.save_pretrained(a.out)
json.dump({"device": dev, "base": a.base, "data": a.data, "rows": len(rows), "epochs": a.epochs, "lr": a.lr, "batch": a.batch, "seconds": round(time.time() - t0)}, open(f"{a.out}/training.json", "w"), indent=1)
print(f"saved {a.out} after {time.time()-t0:.0f}s")
