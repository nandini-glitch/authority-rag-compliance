import os
import time
import re
from typing import List, Dict, Any, Tuple, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from src.parser import RegulatoryMetadata, format_authority_header

def call_with_retry(api_fn, max_retries: int = 8, default_wait: int = 20):
    for attempt in range(max_retries):
        try:
            return api_fn()
        except Exception as e:
            err_str = str(e)
            is_rate_limit = "429" in err_str or "quota" in err_str.lower() or "rate" in err_str.lower() or "resource_exhausted" in err_str.lower()
            is_transient = "503" in err_str or "unavailable" in err_str.lower() or "high demand" in err_str.lower() or "internal" in err_str.lower()
            if is_rate_limit or is_transient:
                match = re.search(r"retry in (\d+(?:\.\d+)?)s", err_str)
                delay = float(match.group(1)) + 3 if match else (default_wait * (attempt + 1))
                print(f"\n[Retryable Error] Waiting {delay:.1f}s before retry (attempt {attempt+1}/{max_retries})...", flush=True)
                time.sleep(delay)
            else:
                raise e
    raise RuntimeError(f"Max retries ({max_retries}) exceeded.")

def init_llm_client(preferred_model: Optional[str] = None):
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    force_gemini = os.getenv("FORCE_GEMINI", "0") == "1"

    if openai_key and not force_gemini and not openai_key.startswith("sk-proj-placeholder"):
        try:
            client = OpenAI(api_key=openai_key)
            model = preferred_model or "gpt-4o"
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=2
            )
            return client, model
        except Exception:
            pass

    if gemini_key:
        client = OpenAI(
            api_key=gemini_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        model = "gemini-3.5-flash-lite"
        return client, model

    raise ValueError("Neither valid OPENAI_API_KEY nor GEMINI_API_KEY found.")

class ComplianceRAGPipeline:
    def __init__(self, vector_store, model_name: Optional[str] = None):
        self.store = vector_store
        self.client, self.model_name = init_llm_client(preferred_model=model_name)

    def build_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]], mode: str) -> Tuple[str, str]:
        context_str = ""
        for idx, doc in enumerate(retrieved_docs, start=1):
            meta = RegulatoryMetadata(**doc["metadata"])
            prefix = format_authority_header(meta, mode=mode)
            context_str += f"--- DOCUMENT {idx} ---\n{prefix}CONTENT: {doc['text']}\n\n"

        base_instruction = (
            "You are an expert Indian Financial Compliance assistant. Answer the user query strictly "
            "based on the provided document excerpts."
        )

        if mode == "naive":
            system_instruction = base_instruction
        elif mode == "recency_only":
            system_instruction = base_instruction + (
                " If documents contradict each other, resolve the contradiction by giving "
                "precedence to the document with the more recent issuance date."
            )
        elif mode == "full":
            system_instruction = base_instruction + (
                " If documents contradict each other, resolve the contradiction by giving strict "
                "precedence to higher Authority Tiers (Tier 1 Regulator > Tier 3 Internal Policy) "
                "and more recent issuance dates."
            )
        else:
            raise ValueError(f"Unknown mode: {mode}")

        user_prompt = f"CONTEXT:\n{context_str}\n\nQUERY: {query}\n\nANSWER:"
        return system_instruction, user_prompt

    def run(self, query: str, top_k: int = 5, mode: str = "full") -> Dict[str, Any]:
        docs = self.store.query(query_text=query, top_k=top_k)
        sys_msg, user_msg = self.build_prompt(query, docs, mode=mode)

        response = call_with_retry(
            lambda: self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.0
            )
        )

        return {
            "query": query,
            "mode": mode,
            "response": response.choices[0].message.content,
            "retrieved_docs": docs,
            "system_prompt": sys_msg,
            "user_prompt": user_msg
        }