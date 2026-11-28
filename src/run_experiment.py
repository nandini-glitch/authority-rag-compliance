import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import json
import time
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from src.parser import ComplianceChunk, RegulatoryMetadata
from src.indexer import ComplianceVectorStore
from src.pipelines import ComplianceRAGPipeline
from src.evaluator import ComplianceEvaluator
from src.benchmark_cases import BENCHMARK_CASES
from src.oracle import OracleStore

MODES = ["naive", "recency_only", "full"]
CATEGORIES = [
    "AUTHORITY_CORRECT_RESOLUTION",
    "FRANKENSTEIN_BLENDING",
    "OUTDATED_RULE_SELECTED",
    "PARAMETRIC_LEAKAGE",
]
CASE_TYPES = ["temporal", "authority", "control"]

TOP_K = int(os.getenv("TOP_K", "15"))
PACE = float(os.getenv("PACE_SECONDS", "3"))   # pause between API calls; raise if you hit rate limits
RETRIEVAL_MODE = os.getenv("RETRIEVAL_MODE", "standard")   # "standard" (vector retrieval) or "oracle" (gold evidence chunks)
assert RETRIEVAL_MODE in ("standard", "oracle"), RETRIEVAL_MODE
RESULTS_DIR = "results" if RETRIEVAL_MODE == "standard" else "results/oracle"

CHUNKS_PATH = "data/parsed_chunks/regulatory_chunks.json"
RESULTS_PATH = f"{RESULTS_DIR}/experiment_results.json"
META_PATH = f"{RESULTS_DIR}/run_meta.json"


def load_chunks(path=CHUNKS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [
        ComplianceChunk(
            chunk_id=c["chunk_id"],
            text=c["text"],
            metadata=RegulatoryMetadata(**c["metadata"])
        )
        for c in raw
    ]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def run_fingerprint(model_name: str) -> dict:
    with open(CHUNKS_PATH, "rb") as f:
        chunks_hash = sha(f.read())
    cases_hash = sha(json.dumps(BENCHMARK_CASES, sort_keys=True).encode("utf-8"))
    return {"model": model_name, "retrieval_mode": RETRIEVAL_MODE, "top_k": TOP_K, "chunks_sha": chunks_hash, "cases_sha": cases_hash}


def empty_stats():
    d = {"total": 0}
    d.update({c: 0 for c in CATEGORIES})
    return d


def pct(n, d):
    return (n / d * 100) if d else 0.0


def build_summaries(results_by_id):
    overall = {m: empty_stats() for m in MODES}
    by_type = {m: {t: empty_stats() for t in CASE_TYPES} for m in MODES}
    valid_ids = {tc["id"] for tc in BENCHMARK_CASES}
    for cid, rec in results_by_id.items():
        if cid not in valid_ids:
            continue
        ctype = rec.get("case_type", "temporal")
        for m in MODES:
            if m not in rec["modes"]:
                continue
            cls = rec["modes"][m]["eval"]["classification"]
            for tgt in (overall[m], by_type[m][ctype]):
                tgt["total"] += 1
                tgt[cls] = tgt.get(cls, 0) + 1
    return overall, by_type


def generate_markdown_report(overall, by_type, detailed_results, meta, out_path):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = []
    md.append("# Experimental Results: Authority-Aware Contradiction Resolution in RAG")
    md.append(f"**Generated:** {ts}  ")
    md.append(f"**Model:** `{meta['model']}`  |  **retrieval:** {meta['retrieval_mode']}  |  **top_k:** {meta['top_k']}  |  **chunks:** `{meta['chunks_sha']}`  |  **cases:** `{meta['cases_sha']}`\n")
    md.append("This file records raw outcomes only. Interpretation belongs in the paper.\n")

    def table(title, rows):
        md.append(f"## {title}\n")
        md.append("| Condition | Correct | Frankenstein Blending | Outdated Rule Selected | Parametric Leakage | n |")
        md.append("|---|---|---|---|---|---|")
        for label, st in rows:
            t = st["total"]
            cells = " | ".join(f"{st[c]}/{t} ({pct(st[c], t):.1f}%)" for c in CATEGORIES)
            md.append(f"| **{label}** | {cells} | {t} |")
        md.append("")

    table("1. Overall", [(m.upper(), overall[m]) for m in MODES])
    for ct in CASE_TYPES:
        table(f"2. Case type: {ct}", [(m.upper(), by_type[m][ct]) for m in MODES])

    md.append("## 3. Case-by-case\n")
    for idx, item in enumerate(detailed_results, start=1):
        md.append(f"### {idx}. {item['topic']} (`{item['id']}`, {item.get('case_type', '?')})")
        md.append(f"**Query:** *{item['query']}*  ")
        md.append(f"**Conflict type:** {item['conflict_type']}  ")
        md.append(f"**Ground truth:**\n> {item['ground_truth']}\n")
        for m in MODES:
            if m not in item["modes"]:
                md.append(f"- **{m}**: *(not yet run)*\n")
                continue
            r = item["modes"][m]
            cls = r["eval"]["classification"]
            badge = "PASS" if cls == "AUTHORITY_CORRECT_RESOLUTION" else "FAIL"
            md.append(f"- **{m}** [{badge}] `{cls}`")
            md.append(f"  - *Judge:* {r['eval']['reasoning']}")
            md.append(f"  - *Output:* {r['response'].strip()}\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Report generated: {out_path}")


def main():
    print("=" * 70)
    print("Authority-Aware Contradiction Resolution Experiment")
    print("=" * 70)

    chunks = load_chunks()
    print(f"Loaded {len(chunks)} parsed compliance chunks.")

    if RETRIEVAL_MODE == "oracle":
        raw_chunks = json.load(open(CHUNKS_PATH, encoding="utf-8"))
        store = OracleStore(BENCHMARK_CASES, raw_chunks)
        print("ORACLE mode: gold evidence chunks are supplied directly (no retrieval).")
    else:
        store = ComplianceVectorStore()
        store.reset()
        store.add_chunks(chunks)
        print(f"Indexed {store.collection.count()} chunks into ChromaDB.")

    pipeline = ComplianceRAGPipeline(vector_store=store)
    evaluator = ComplianceEvaluator()
    print(f"Pipeline & Evaluator initialized using model: {pipeline.model_name}")

    # ---- guard against mixing runs from different corpora / cases / models ----
    meta = run_fingerprint(pipeline.model_name)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    if os.path.exists(RESULTS_PATH):
        if not os.path.exists(META_PATH):
            sys.exit("\nresults/experiment_results.json exists from an older run (no run_meta.json).\n"
                     "Delete results/*.json and re-run, so old and new results are never mixed.")
        old_meta = json.load(open(META_PATH, encoding="utf-8"))
        if old_meta != meta:
            diff = {k: (old_meta.get(k), meta[k]) for k in meta if old_meta.get(k) != meta[k]}
            sys.exit(f"\nSaved results were produced under a different setup: {diff}\n"
                     "Delete results/*.json to start a clean run (or restore the previous setup to resume).")
    json.dump(meta, open(META_PATH, "w", encoding="utf-8"), indent=2)

    results_by_id = {}
    if os.path.exists(RESULTS_PATH):
        for r in json.load(open(RESULTS_PATH, encoding="utf-8")):
            results_by_id[r["id"]] = r
        print(f"Loaded existing progress for {len(results_by_id)} case(s).")

    def save_progress():
        ordered = [results_by_id[tc["id"]] for tc in BENCHMARK_CASES if tc["id"] in results_by_id]
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(ordered, f, indent=2)

    print(f"\nRunning benchmark suite ({len(BENCHMARK_CASES)} cases x {len(MODES)} modes), top_k={TOP_K}, pace={PACE}s")

    for tc in BENCHMARK_CASES:
        if tc["id"] not in results_by_id:
            results_by_id[tc["id"]] = {
                "id": tc["id"],
                "case_type": tc["case_type"],
                "topic": tc["topic"],
                "conflict_type": tc["conflict_type"],
                "query": tc["query"],
                "ground_truth": tc["ground_truth"],
                "modes": {}
            }
        case_record = results_by_id[tc["id"]]

        print(f"\n[{tc['id']}] ({tc['case_type']}) {tc['topic']}")

        for mode in MODES:
            if mode in case_record["modes"]:
                print(f"  {mode}: already done, skipping")
                continue

            print(f"  {mode}...", end="", flush=True)
            t0 = time.time()
            res = pipeline.run(query=tc["query"], top_k=TOP_K, mode=mode)
            gen_latency = time.time() - t0
            time.sleep(PACE)

            t_eval = time.time()
            eval_res = evaluator.evaluate_response(
                query=tc["query"],
                ground_truth=tc["ground_truth"],
                generated_response=res["response"]
            )
            eval_latency = time.time() - t_eval

            docs = res["retrieved_docs"]
            case_record["modes"][mode] = {
                "response": res["response"],
                "latency_sec": round(gen_latency + eval_latency, 2),
                "eval": eval_res,
                "retrieved_doc_ids": [d["metadata"]["doc_id"] for d in docs],
                "retrieved_chunk_ids": [d["id"] for d in docs] if docs and "id" in docs[0] else []
            }
            print(f" -> {eval_res.get('classification')} (gen {gen_latency:.1f}s, eval {eval_latency:.1f}s)")
            save_progress()
            time.sleep(PACE)

    overall, by_type = build_summaries(results_by_id)
    with open(f"{RESULTS_DIR}/evaluation_summary.json", "w", encoding="utf-8") as f:
        json.dump(overall, f, indent=2)
    with open(f"{RESULTS_DIR}/evaluation_by_type.json", "w", encoding="utf-8") as f:
        json.dump(by_type, f, indent=2)

    detailed = [results_by_id[tc["id"]] for tc in BENCHMARK_CASES if tc["id"] in results_by_id]
    generate_markdown_report(overall, by_type, detailed, meta, f"{RESULTS_DIR}/OBSERVATIONS.md")

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE (or paused - re-run the same command to continue)")
    print("=" * 70)
    for m in MODES:
        st = overall[m]
        print(f"  {m.upper():<13} correct {st['AUTHORITY_CORRECT_RESOLUTION']}/{st['total']} ({pct(st['AUTHORITY_CORRECT_RESOLUTION'], st['total']):.1f}%)"
              f" | blend {st['FRANKENSTEIN_BLENDING']} | outdated {st['OUTDATED_RULE_SELECTED']} | parametric {st['PARAMETRIC_LEAKAGE']}")
    print("\nBy case type (correct / n):")
    for ct in CASE_TYPES:
        row = "  ".join(f"{m}: {by_type[m][ct]['AUTHORITY_CORRECT_RESOLUTION']}/{by_type[m][ct]['total']}" for m in MODES)
        print(f"  {ct:<10} {row}")


if __name__ == "__main__":
    main()
