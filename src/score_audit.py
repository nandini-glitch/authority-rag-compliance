"""
Compares your blind human labels with the LLM judge.

Usage: python -m src.score_audit       (add RETRIEVAL_MODE=oracle for results/oracle/)
Reports: agreement and Cohen's kappa on correct-vs-incorrect, human accuracy per condition next to
the judge's, and what you labelled the answers the judge called FRANKENSTEIN_BLENDING.
"""
import csv
import json
import os
from collections import Counter

RESULTS_DIR = "results/oracle" if os.getenv("RETRIEVAL_MODE") == "oracle" else "results"
ALLOWED = {"CORRECT", "WRONG_RULE", "UNRESOLVED", "BLEND", "OTHER"}
OK = "AUTHORITY_CORRECT_RESOLUTION"


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pa, pb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((pa[x] / n) * (pb[x] / n) for x in (0, 1))
    return None if pe == 1 else (po - pe) / (1 - pe)


def main():
    sheet = {r["audit_id"]: r for r in csv.DictReader(open(f"{RESULTS_DIR}/audit_sheet.csv", encoding="utf-8"))}
    key = {r["audit_id"]: r for r in csv.DictReader(open(f"{RESULTS_DIR}/audit_key.csv", encoding="utf-8"))}

    bad = [a for a, r in sheet.items() if r["human_label"].strip().upper() not in ALLOWED]
    if bad:
        raise SystemExit(f"{len(bad)} rows have a missing/invalid human_label (allowed: {sorted(ALLOWED)}). First: {bad[:5]}")

    rows = []
    for aid, r in sheet.items():
        h = r["human_label"].strip().upper()
        rows.append({"id": aid, "human": h, "judge": key[aid]["judge_label"], "mode": key[aid]["mode"],
                     "case": key[aid]["case_id"]})

    pairs = [(int(x["human"] == "CORRECT"), int(x["judge"] == OK)) for x in rows]
    n = len(rows)
    agree = sum(a == b for a, b in pairs)
    k = kappa(pairs)
    print(f"Audited answers: {n}")
    print(f"Correct-vs-incorrect agreement: {agree}/{n} ({agree / n * 100:.1f}%)   Cohen's kappa: " + ("undefined" if k is None else f"{k:.2f}"))

    print("\nConfusion (rows = human, cols = judge):")
    print(f"  {'':<18}{'judge correct':>15}{'judge incorrect':>17}")
    for hv, name in ((1, "human correct"), (0, "human incorrect")):
        print(f"  {name:<18}{sum(1 for a, b in pairs if a == hv and b == 1):>15}{sum(1 for a, b in pairs if a == hv and b == 0):>17}")

    print("\nAccuracy per condition in the audited sample (human vs judge):")
    for m in ("naive", "recency_only", "full"):
        sub = [x for x in rows if x["mode"] == m]
        if sub:
            h = sum(x["human"] == "CORRECT" for x in sub)
            j = sum(x["judge"] == OK for x in sub)
            print(f"  {m:<14} human {h}/{len(sub)}   judge {j}/{len(sub)}")

    blends = [x["human"] for x in rows if x["judge"] == "FRANKENSTEIN_BLENDING"]
    if blends:
        print(f"\nAnswers the judge called FRANKENSTEIN_BLENDING ({len(blends)}): you labelled them {dict(Counter(blends))}")

    json.dump({"n": n, "agreement": agree / n, "kappa": k, "rows": rows}, open(f"{RESULTS_DIR}/audit_scores.json", "w"), indent=2)
    print(f"\nWrote {RESULTS_DIR}/audit_scores.json")


if __name__ == "__main__":
    main()
