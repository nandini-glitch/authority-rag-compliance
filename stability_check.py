import json
from dotenv import load_dotenv
load_dotenv()
from src.parser import ComplianceChunk, RegulatoryMetadata
from src.indexer import ComplianceVectorStore
from src.pipelines import ComplianceRAGPipeline
from src.evaluator import ComplianceEvaluator

chunks_raw = json.load(open("data/parsed_chunks/regulatory_chunks.json"))
chunks = [ComplianceChunk(chunk_id=c["chunk_id"], text=c["text"], metadata=RegulatoryMetadata(**c["metadata"])) for c in chunks_raw]

store = ComplianceVectorStore()
store.reset()
store.add_chunks(chunks)

pipeline = ComplianceRAGPipeline(vector_store=store)
evaluator = ComplianceEvaluator()

query = "What is the maximum permissible Default Loss Guarantee (DLG / FLDG) coverage that can be accepted from a Lending Service Provider (LSP)? Can a bank internal policy permit up to 10%?"
ground_truth = ("Under RBI Directions 2025 (Tier 1 Statutory Regulator, RBI/2025-26/36, Chapter VI, Para 20), "
    "the total DLG cover across all portfolio arrangements shall not exceed 5.0% of the total disbursed loan portfolio. "
    "An internal bank policy or SOP (Tier 3, such as Apex Bank SOP 2024 permitting 10%) is subordinate to RBI regulations "
    "and legally void to the extent of the conflict. The cap remains strictly 5%.")

for i in range(3):
    res = pipeline.run(query=query, top_k=15, mode="full")
    ev = evaluator.evaluate_response(query=query, ground_truth=ground_truth, generated_response=res["response"])
    print(f"Run {i+1}: {ev['classification']}")
