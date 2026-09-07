import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

from src.parser import ComplianceChunk, format_authority_header

def get_embedding_function(provider: str = "auto"):
    load_dotenv()
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                fn = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=api_key,
                    model_name="text-embedding-3-small"
                )
                # Quick test call to ensure quota exists
                fn(["test"])
                return fn
            except Exception as e:
                print(f"[indexer] OpenAI embedding unavailable ({e}). Falling back to local DefaultEmbeddingFunction.")
    return embedding_functions.DefaultEmbeddingFunction()

class ComplianceVectorStore:
    def __init__(self, collection_name: str = "indian_financial_compliance", persist_dir: str = "./chroma_db", embedding_provider: str = "auto"):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_fn = get_embedding_function(embedding_provider)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def reset(self):
        """Deletes and recreates the collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[ComplianceChunk]):
        if not chunks:
            return

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            documents.append(chunk.text)
            meta_dict = chunk.metadata.model_dump()
            # ChromaDB requires metadata values to be str, int, float, or bool.
            # Convert any None values to empty strings.
            sanitized_meta = {
                k: ("" if v is None else v)
                for k, v in meta_dict.items()
            }
            metadatas.append(sanitized_meta)
            ids.append(chunk.chunk_id)

        # Use upsert to handle re-runs idempotently without DuplicateIDError
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        total_docs = self.collection.count()
        if total_docs == 0:
            return []

        actual_k = min(top_k, total_docs)
        results = self.collection.query(
            query_texts=[query_text],
            n_results=actual_k
        )

        retrieved_docs = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                retrieved_docs.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i]
                })
        return retrieved_docs