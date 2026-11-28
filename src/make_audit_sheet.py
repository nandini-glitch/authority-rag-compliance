"""
Builds a BLIND human-audit sheet: a random sample of answers with the condition and the judge's
label hidden. You label them, then score_audit.py compares your labels with the LLM judge.

Usage:
    python -m src.make_audit_sheet                         # results/
    RETRIEVAL_MODE=oracle python -m src.make_audit_sheet   # results/oracle/
Writes <dir>/audit_sheet.csv (fill the human_label column) and <dir>/audit_key.csv (do NOT open
until you have finished labelling).
"""
import csv
import json
import os
import random

RESULTS_DIR = "results/oracle" if os.getenv("RETRIEVAL_MODE") == "oracle" else "results"
MODES = ["naive", "recency_only", "full"]
N_PER_MODE = int(os.getenv("AUDIT_PER_MODE", "8"))
SEED = int(os.getenv("AUDIT_SEED", "7"))

GUIDE = """
LABELS (type exactly one in the human_label column):
  CORRECT     gives the answer in the ground truth AND treats the conflicting superseded or
              lower-authority rule as not applicable
  WRONG_RULE  commits to the superseded or lower-authority rule as the answer
  UNRESOLVED  reports both rules/sources without committing to which one applies
  BLEND       invents a compromise or mixed rule that neither source states
  OTHER       anything else (ignores the sources, off-topic, refuses)
Judge the answer against the ground_truth column only. Do not guess which condition produced it.
"""


def main():
    results = json.load(open(f"{RESULTS_DIR}/experiment_results.json", encoding="utf-8"))
    rng = random.Random(SEED)
    picked = []
    for m in MODES:
        pool = [(r, m) for r in results if m in r["modes"]]
        picked += rng.sample(pool, min(N_PER_MODE, len(pool)))
    rng.shuffle(picked)

    with open(f"{RESULTS_DIR}/audit_sheet.csv", "w", newline="", encoding="utf-8") as f, \
         open(f"{RESULTS_DIR}/audit_key.csv", "w", newline="", encoding="utf-8") as k:
        w, kw = csv.writer(f), csv.writer(k)
        w.writerow(["audit_id", "query", "ground_truth", "answer", "human_label", "notes"])
        kw.writerow(["audit_id", "case_id", "case_type", "mode", "judge_label"])
        for i, (r, m) in enumerate(picked, start=1):
            aid = f"A{i:03d}"
            w.writerow([aid, r["query"], r["ground_truth"], r["modes"][m]["response"].strip(), "", ""])
            kw.writerow([aid, r["id"], r.get("case_type", ""), m, r["modes"][m]["eval"]["classification"]])

    print(f"Wrote {len(picked)} answers to {RESULTS_DIR}/audit_sheet.csv (blind) and audit_key.csv")
    print(GUIDE)


if __name__ == "__main__":
    main()
