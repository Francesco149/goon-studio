import json, os
base = os.path.expanduser("~/goonlab/jobs")
out = []
for name in ("e6.jsonl", "e7.jsonl"):
    with open(os.path.join(base, name), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
with open(os.path.join(base, "e67.jsonl"), "w", encoding="utf-8") as fh:
    for j in out:
        fh.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(out))
