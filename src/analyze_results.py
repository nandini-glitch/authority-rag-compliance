"""
Case-level breakdown of results/experiment_results.json.

  - table of outcome per case x condition
  - whether the evidence chunks for each case were actually retrieved (retrieval is identical
    across conditions, so this separates retrieval misses from reasoning failures)
  - judge reasoning + response for every FULL-mode failure
  - writes results/case_level.csv (used later for plots and paired significance tests)

Usage: python -m src.analyze_results
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.benchmark_cases import BENCHMARK_CASES

RESULTS_DIR = "results/oracle" if os.getenv("RETRIEVAL_MODE") == "oracle" else "results"
MODES = ["naive", "recency_only", "full"]
CODE = {"AUTHORITY_CORRECT_RESOLUTION": "OK", "FRANKENSTEIN_BLENDING": "BLEND",
        "OUTDATED_RULE_SELECTED": "OUTD", "PARAMETRIC_LEAKAGE": "PARAM"}


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    chunks = json.load(open("data/parsed_chunks/regulatory_chunks.json", encoding="utf-8"))
    results = {r["id"]: r for r in json.load(open(f"{RESULTS_DIR}/experiment_results.json", encoding="utf-8"))}

    rows = []
    print(f"{'case':<32}{'type':<10}{'naive':<8}{'recency':<9}{'full':<8}{'evidence retrieved'}")
    print("-" * 85)
    for tc in BENCHMARK_CASES:
        r = results.get(tc["id"])
        if not r:
            print(f"{tc['id']:<32}(not run)")
            continue
        retrieved = set()
        for m in MODES:
            retrieved |= set(r["modes"].get(m, {}).get("retrieved_chunk_ids", []))
        have_ids = bool(retrieved)

        found = 0
        for doc, quote in tc["evidence"]:
            hit_ids = {c["chunk_id"] for c in chunks if c["metadata"]["doc_id"] == doc and norm(quote) in norm(c["text"])}
            if hit_ids & retrieved:
                found += 1
        ev = f"{found}/{len(tc['evidence'])}" if have_ids else "n/a (no chunk ids saved)"

        codes = [CODE.get(r["modes"][m]["eval"]["classification"], "?") if m in r["modes"] else "-" for m in MODES]
        print(f"{tc['id']:<32}{tc['case_type']:<10}{codes[0]:<8}{codes[1]:<9}{codes[2]:<8}{ev}")
        rows.append([tc["id"], tc["case_type"], *codes, ev])

    with open(f"{RESULTS_DIR}/case_level.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "case_type", "naive", "recency_only", "full", "evidence_retrieved"])
        w.writerows(rows)
    print(f"\nWrote {RESULTS_DIR}/case_level.csv")

    print("\n" + "=" * 85)
    print("FULL-MODE FAILURES")
    print("=" * 85)
    any_fail = False
    for tc in BENCHMARK_CASES:
        r = results.get(tc["id"])
        if not r or "full" not in r["modes"]:
            continue
        f = r["modes"]["full"]
        if f["eval"]["classification"] != "AUTHORITY_CORRECT_RESOLUTION":
            any_fail = True
            print(f"\n[{tc['id']}] {f['eval']['classification']}")
            print("QUERY :", tc["query"])
            print("JUDGE :", f["eval"]["reasoning"])
            print("ANSWER:", f["response"].strip()[:900])
    if not any_fail:
        print("none")


if __name__ == "__main__":
    main()
