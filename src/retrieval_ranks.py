"""
Where does each evidence chunk rank for its query (out of all indexed chunks)?
Retrieval only: no LLM calls, no API cost.

Usage: python -m src.retrieval_ranks
"""
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv()

from src.benchmark_cases import BENCHMARK_CASES
from src.parser import ComplianceChunk, RegulatoryMetadata
from src.indexer import ComplianceVectorStore

K_PRIMARY = 15


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    raw = json.load(open("data/parsed_chunks/regulatory_chunks.json", encoding="utf-8"))
    store = ComplianceVectorStore()
    store.reset()
    store.add_chunks([ComplianceChunk(chunk_id=c["chunk_id"], text=c["text"],
                                      metadata=RegulatoryMetadata(**c["metadata"])) for c in raw])
    n = len(raw)

    print(f"{'case':<32}{'doc':<6}{'rank':>5}  {'@15':<8}evidence")
    print("-" * 100)
    worst_per_case = {}
    for tc in BENCHMARK_CASES:
        ranked = [d["id"] for d in store.query(query_text=tc["query"], top_k=n)]
        pos = {cid: i + 1 for i, cid in enumerate(ranked)}
        worst = 0
        for doc, quote in tc["evidence"]:
            hits = [c["chunk_id"] for c in raw if c["metadata"]["doc_id"] == doc and norm(quote) in norm(c["text"])]
            ranks = [pos[h] for h in hits if h in pos]
            rank = min(ranks) if ranks else n + 1
            worst = max(worst, rank)
            flag = "ok" if rank <= K_PRIMARY else "MISS"
            print(f"{tc['id']:<32}{doc.split('/')[0]:<6}{rank:>5}  {flag:<8}{quote[:48]}")
        worst_per_case[tc["id"]] = worst

    print("\nCases whose evidence is fully inside top-k:")
    for k in (10, 15, 20, 25, 30, 40):
        ok = sum(1 for v in worst_per_case.values() if v <= k)
        print(f"  k={k:<3} {ok}/{len(worst_per_case)}")


if __name__ == "__main__":
    main()
