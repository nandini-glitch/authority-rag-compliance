import os
from typing import List, Dict, Any
from openai import OpenAI
from src.parser import RegulatoryMetadata, format_authority_header

class ComplianceRAGPipeline:
    def __init__(self, vector_store, model_name: str = "gpt-4o"):
        self.store = vector_store
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def build_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]], mode: str) -> str:
        context_str = ""
        for idx, doc in enumerate(retrieved_docs, start=1):
            meta = RegulatoryMetadata(**doc["metadata"])
            prefix = format_authority_header(meta, mode=mode)
            context_str += f"--- DOCUMENT {idx} ---\n{prefix}CONTENT: {doc['text']}\n\n"

        system_instruction = (
            "You are an expert Indian Financial Compliance assistant. Answer the user query strictly "
            "based on the provided document excerpts. If documents contradict each other, resolve the contradiction "
            "by giving strict precedence to higher Authority Tiers (Tier 1 Regulator > Tier 3 Internal Policy) "
            "and more recent issuance dates."
        )

        user_prompt = f"CONTEXT:\n{context_str}\n\nQUERY: {query}\n\nANSWER:"
        return system_instruction, user_prompt

    def run(self, query: str, top_k: int = 5, mode: str = "full") -> Dict[str, Any]:
        docs = self.store.query(query_text=query, top_k=top_k)
        sys_msg, user_msg = self.build_prompt(query, docs, mode=mode)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.0
        )

        return {
            "query": query,
            "mode": mode,
            "response": response.choices[0].message.content,
            "retrieved_docs": docs
        }