import chromadb
from chromadb.utils import embedding_functions
from typing import List
from src.parser import ComplianceChunk, format_authority_header

class ComplianceVectorStore:
    def __init__(self, collection_name: str = "indian_financial_compliance", persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        # Using default embeddings or OpenAI embedding function
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[ComplianceChunk]):
        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:
            documents.append(chunk.text)
            # Flatten metadata dict for Chroma storage
            meta_dict = chunk.metadata.model_dump()
            metadatas.append(meta_dict)
            ids.append(chunk.chunk_id)

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        
        retrieved_docs = []
        if results and results["documents"]:
            for i in range(len(results["documents"][0])):
                retrieved_docs.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i]
                })
        return retrieved_docs