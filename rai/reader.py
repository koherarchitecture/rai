"""The reader only points: given a question and a typed answer, the phrase in the answer that answers it, or nothing.
Extractive (deepset/minilm-uncased-squad2 by default); it has no vocabulary to write with."""
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers.utils import logging
logging.set_verbosity_error()
torch.set_num_threads(4)

BASE = "deepset/minilm-uncased-squad2"
MAX_SPAN = 30


class Reader:
    def __init__(self, model=BASE):
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model).eval()

    def read(self, question, answer, stem=""):
        """Returns (span, margin). span is None when the reader finds no answer.
        The stem is a reading aid prepended before reading; the span is checked against the typed answer alone."""
        text = stem + answer if stem and not answer.lower().startswith(stem.strip().lower()) else answer
        enc = self.tok(question, text, return_tensors="pt", truncation="only_second", max_length=384, stride=128,
                       return_overflowing_tokens=True)
        best, null = -1e9, 1e9
        best_ids = None
        with torch.no_grad():
            out = self.model(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"])
        for w in range(enc["input_ids"].shape[0]):           # one window at a time; the answer counts if any window finds it
            s, e = out.start_logits[w], out.end_logits[w]
            ctx = [i for i, sid in enumerate(enc.sequence_ids(w)) if sid == 1]
            score, i, j = max(((s[i] + e[j]).item(), i, j) for i in ctx for j in ctx if i <= j < i + MAX_SPAN)
            null = min(null, (s[0] + e[0]).item())
            if score > best:
                best, best_ids = score, enc["input_ids"][w][i:j + 1]
        span = self.tok.decode(best_ids).strip()
        margin = best - null
        if margin <= 0 or span.lower() not in answer.lower():   # the verbatim guard: the phrase must be in what was typed
            return None, margin
        return span, margin
