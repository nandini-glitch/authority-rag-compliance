"""
Paired exact McNemar tests between conditions (same 17 cases answered under each condition).

Usage:
    python -m src.paired_tests                          # results/
    RETRIEVAL_MODE=oracle python -m src.paired_tests    # results/oracle/
"""
import json
import os
from itertools import combinations
from math import comb

RESULTS_DIR = "results/oracle" if os.getenv("RETRIEVAL_MODE") == "oracle" else "results"
MODES = ["naive", "recency_only", "full"]
OK = "AUTHORITY_CORRECT_RESOLUTION"


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact binomial test on the discordant pairs (b = A-only correct, c = B-only correct)."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m, out, running = len(items), {}, 0.0
    for i, (name, p) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        out[name] = running
    return out


def run(results, subset=None, label="all cases"):
    rows = [r for r in results if subset is None or r.get("case_type") == subset]
    correct = {m: {r["id"]: r["modes"][m]["eval"]["classification"] == OK for r in rows if m in r["modes"]} for m in MODES}
    print(f"\n{label} (n={len(rows)})")
    print("  accuracy: " + "   ".join(f"{m} {sum(correct[m].values())}/{len(correct[m])}" for m in MODES))
    raw, detail = {}, {}
    for a, b_ in combinations(MODES, 2):
        ids = [i for i in correct[a] if i in correct[b_]]
        only_a = sum(1 for i in ids if correct[a][i] and not correct[b_][i])
        only_b = sum(1 for i in ids if correct[b_][i] and not correct[a][i])
        key = f"{a} vs {b_}"
        raw[key] = mcnemar_exact(only_a, only_b)
        detail[key] = (only_a, only_b)
    adj = holm(raw)
    print(f"  {'comparison':<24}{'A-only':>7}{'B-only':>8}{'p (exact)':>12}{'p (Holm)':>11}")
    for key in raw:
        a_only, b_only = detail[key]
        print(f"  {key:<24}{a_only:>7}{b_only:>8}{raw[key]:>12.4f}{adj[key]:>11.4f}")


def main():
    results = json.load(open(f"{RESULTS_DIR}/experiment_results.json", encoding="utf-8"))
    print(f"Results dir: {RESULTS_DIR}")
    run(results)
    run(results, "authority", "authority cases only")
    print("\nA-only = cases only the first condition got right; B-only = only the second.")
    print("Holm correction covers the 3 pairwise comparisons within each block.")


if __name__ == "__main__":
    main()
