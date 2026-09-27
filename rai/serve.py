"""Keyed inference for rai: read_answers over HTTP, for programs Koher runs (rai ka pahad first). Not open to the world.
Prayas, 27 September 2026: "part of koher engine core - called by api key in rai ka pahad - keyed inference - not free and open to world",
and "server deploy not browser". A request without the key gets 401 and is not read.

POST /read_answers   header X-API-Key: <RAI_API_KEY>
  {"questions": [{"id": "q1", "text": "who fills it", "stem": ""}, ...], "answers": {"q1": "sunil bhai fills it", ...}}
  -> {"found": {"q1": true, ...}}          (rai.ask.read_answers at rai's current READER and THRESHOLD)
GET /health -> {"reader": "rai-0.3.7", "threshold": 8.92}

Nothing is kept: no answer is stored and no request is logged (GUIDELINE.md, line 6).
usage: RAI_API_KEY=... python -m rai.serve [port]"""
import hmac, json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .ask import read_answers, READER, THRESHOLD
from .reader import Reader

KEY = os.environ["RAI_API_KEY"]
reader = Reader(READER)


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self.send(200, {"reader": os.path.basename(READER), "threshold": THRESHOLD})
        self.send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/read_answers":
            return self.send(404, {"error": "not found"})
        if not hmac.compare_digest(self.headers.get("X-API-Key", ""), KEY):
            return self.send(401, {"error": "a key is needed"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            whole = {"notion": "", "questions": [{"id": q["id"], "text": q["text"], "stem": q.get("stem", "")} for q in body["questions"]]}
            found = read_answers(whole, {k: str(v) for k, v in body["answers"].items()}, reader, THRESHOLD)
        except (KeyError, TypeError, ValueError):
            return self.send(400, {"error": "questions and answers are needed"})
        self.send(200, {"found": found})

    def log_message(self, *args):   # nothing is logged
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", int(sys.argv[1]) if len(sys.argv) > 1 else 8080), Handler).serve_forever()
