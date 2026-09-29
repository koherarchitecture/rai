"""Train rai with a Hinglish teacher beside it (0.3.8). The student is deepset's MiniLM trained on 0.3.7's rows and the Hinglish rows
(data/train-synth.jsonl, data/train-hinglish.jsonl) at 0.3.7's recipe, 2 passes at 2e-5, batch 32. On the Hinglish rows it also learns
the teacher's start and end scores: both sides' scores are standardised over each row's real tokens (mean 0, spread 1; Sun et al. 2024,
Logit Standardization in Knowledge Distillation) and matched by mean squared error (Kim et al. 2021), added to the ordinary loss. The
teacher is HingBERT (l3cube-pune/hing-bert, CC-BY-4.0) taught to point by scripts/train-full.sh; it shares MiniLM's vocabulary piece
for piece, so its scores line up token by token. Standardising matters: matching the raw scores made the student confident about
vague answers and the count collapsed. On the English rows only the ordinary labels teach.
usage: python scripts/distil.py --teacher runs/teacher --out runs/rai-0.3.8-seed7 --seed 7"""
import argparse, json, random, time
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

ap = argparse.ArgumentParser()
ap.add_argument("--teacher", required=True); ap.add_argument("--out", required=True); ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()
BASE = "deepset/minilm-uncased-squad2"
torch.manual_seed(a.seed); random.seed(a.seed)
dev = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

rows = [dict(json.loads(l), kd=False) for l in open("data/train-synth.jsonl")] + [dict(json.loads(l), kd=True) for l in open("data/train-hinglish.jsonl")]
tok = AutoTokenizer.from_pretrained(BASE)
student = AutoModelForQuestionAnswering.from_pretrained(BASE).to(dev)
teacher = AutoModelForQuestionAnswering.from_pretrained(a.teacher).to(dev).eval()


def features(batch):   # rai/train.py's, with the Hinglish mark carried along
    texts = [(r["stem"] + r["answer"]) if r["stem"] and not r["answer"].lower().startswith(r["stem"].strip().lower()) else r["answer"] for r in batch]
    enc = tok([r["question"] for r in batch], texts, truncation="only_second", max_length=384, padding=True, return_offsets_mapping=True, return_tensors="pt")
    starts, ends = [], []
    for i, r in enumerate(batch):
        s = e = 0
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
    enc["kd"] = torch.tensor([r["kd"] for r in batch])
    return enc


def gap(s, t, keep, kd):   # squared difference of standardised scores, over real tokens, averaged over the Hinglish rows
    z = lambda x: ((x - (x * keep).sum(-1, keepdim=True) / keep.sum(-1, keepdim=True)) * keep)
    zs, zt = z(s), z(t)
    zs = zs / ((zs ** 2).sum(-1, keepdim=True) / keep.sum(-1, keepdim=True)).sqrt().clamp(min=1e-6)
    zt = zt / ((zt ** 2).sum(-1, keepdim=True) / keep.sum(-1, keepdim=True)).sqrt().clamp(min=1e-6)
    return ((((zs - zt) ** 2) * keep).sum(-1) / keep.sum(-1) * kd).sum() / kd.sum()


opt = torch.optim.AdamW(student.parameters(), lr=2e-5)
loader = DataLoader(rows, batch_size=32, shuffle=True, collate_fn=features)
student.train(); t0 = time.time(); step = 0
for ep in range(2):
    for batch in loader:
        kd = batch.pop("kd").float().to(dev); batch = {k: v.to(dev) for k, v in batch.items()}
        out = student(**batch)
        loss = out.loss
        if kd.any():
            with torch.no_grad():
                t = teacher(**{k: v for k, v in batch.items() if k not in ("start_positions", "end_positions")})
            keep = batch["attention_mask"].float()
            loss = loss + (gap(out.start_logits, t.start_logits, keep, kd) + gap(out.end_logits, t.end_logits, keep, kd)) / 2
        loss.backward(); opt.step(); opt.zero_grad(); step += 1
        if step % 50 == 0: print(f"epoch {ep+1} step {step} loss {loss.item():.3f} {time.time()-t0:.0f}s", flush=True)
student.save_pretrained(a.out); tok.save_pretrained(a.out)
json.dump({"device": dev, "base": BASE, "teacher": a.teacher, "rows": len(rows), "hinglish_rows": sum(r["kd"] for r in rows), "seed": a.seed, "seconds": round(time.time() - t0)}, open(f"{a.out}/training.json", "w"), indent=1)
print(f"saved {a.out} after {time.time()-t0:.0f}s")
