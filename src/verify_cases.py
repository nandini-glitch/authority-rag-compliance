"""
Checks that every ground-truth evidence quote exists verbatim inside a single indexed chunk
of the named document, and that every claimed absence ('absent') really is absent.

Usage:
    python -m src.verify_cases                  # text check only (offline, instant)
    python -m src.verify_cases --retrieval      # also checks each evidence chunk is inside top-k

Exit code is non-zero if anything fails, so it can gate a run.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.benchmark_cases import BENCHMARK_CASES


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", default="data/parsed_chunks/regulatory_chunks.json")
    ap.add_argument("--retrieval", action="store_true")
    ap.add_argument("--top_k", type=int, default=15)
    args = ap.parse_args()

    chunks = json.load(open(args.chunks, encoding="utf-8"))
    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c["metadata"]["doc_id"], []).append(c)

    failures = 0
    evidence_ids = {}  # case id -> list of (doc, chunk_id)

    for tc in BENCHMARK_CASES:
        for doc, quote in tc["evidence"]:
            hits = [c for c in by_doc.get(doc, []) if norm(quote) in norm(c["text"])]
            if not hits:
                failures += 1
                print(f"FAIL  {tc['id']:<30} [{doc}] quote not found in any single chunk: {quote!r}")
            else:
                evidence_ids.setdefault(tc["id"], []).extend((doc, h["chunk_id"]) for h in hits)
        for doc, token in tc.get("absent", []):
            full = " ".join(norm(c["text"]) for c in by_doc.get(doc, []))
            if norm(token) in full:
                failures += 1
                print(f"FAIL  {tc['id']:<30} [{doc}] expected ABSENT but found: {token!r}")

    if not failures:
        print(f"OK: all evidence quotes verified across {len(BENCHMARK_CASES)} cases.")

    if args.retrieval:
        from dotenv import load_dotenv
        load_dotenv()
        from src.parser import ComplianceChunk, RegulatoryMetadata
        from src.indexer import ComplianceVectorStore

        store = ComplianceVectorStore()
        store.reset()
        store.add_chunks([ComplianceChunk(chunk_id=c["chunk_id"], text=c["text"],
                                          metadata=RegulatoryMetadata(**c["metadata"])) for c in chunks])
        print(f"\nRetrieval check (top_k={args.top_k}): is every evidence chunk retrieved?")
        for tc in BENCHMARK_CASES:
            res = store.query(query_text=tc["query"], top_k=args.top_k)
            got = {d["id"] for d in res} if res and "id" in res[0] else set()
            for doc, cid in evidence_ids.get(tc["id"], []):
                status = "ok  " if cid in got else "MISS"
                if status == "MISS":
                    failures += 1
                print(f"  {status} {tc['id']:<30} {cid}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
