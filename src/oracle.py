"""
Oracle-context ablation: instead of retrieving, hand the model each case's gold evidence chunks
(every chunk named in the case's `evidence` list, i.e. both sides of the conflict).

This removes retrieval noise so the three conditions differ ONLY in the metadata/instructions shown.
Chunk order is a seeded shuffle per case (deterministic) so no document is systematically first.
"""
import random
import re


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"\s+", " ", s).strip().lower()


def _to_doc(c: dict) -> dict:
    # mirror the sanitising done when chunks are written to ChromaDB (None -> "")
    meta = {k: ("" if v is None else v) for k, v in c["metadata"].items()}
    return {"id": c["chunk_id"], "text": c["text"], "metadata": meta}


def evidence_docs(tc: dict, chunks_raw: list) -> list:
    seen, docs = set(), []
    for doc_id, quote in tc["evidence"]:
        for c in chunks_raw:
            if c["metadata"]["doc_id"] == doc_id and norm(quote) in norm(c["text"]):
                if c["chunk_id"] not in seen:
                    seen.add(c["chunk_id"])
                    docs.append(_to_doc(c))
                break
        else:
            raise ValueError(f"{tc['id']}: evidence not found in chunks: {quote!r}")
    random.Random(tc["id"]).shuffle(docs)
    return docs


class OracleStore:
    """Drop-in for ComplianceVectorStore.query(): returns the gold chunks for a known query."""

    def __init__(self, cases: list, chunks_raw: list):
        self.mapping = {tc["query"]: evidence_docs(tc, chunks_raw) for tc in cases}

    def query(self, query_text: str, top_k: int = 5):
        return self.mapping[query_text]
