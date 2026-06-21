#!/usr/bin/env python3
"""
RAG Search Script
Searches ingested documents in ChromaDB using semantic similarity.
"""

import sys
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path


class RAGSearcher:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.persist_dir = Path(persist_dir)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_collection(name="rag_documents")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query: str, top_k: int = 5) -> list:
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )

        search_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else None
                search_results.append({
                    "rank": i + 1,
                    "document": doc or "",
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": distance
                })
        return search_results

    def get_collection_info(self) -> dict:
        count = self.collection.count()
        return {
            "name": self.collection.name,
            "count": count
        }


def main():
    print("=" * 60)
    print("RAG Search Script")
    print("=" * 60)

    searcher = RAGSearcher(persist_dir="./chroma_db")
    info = searcher.get_collection_info()

    if info["count"] == 0:
        print(f"\nError: No documents found. Run 'python ingest.py' first.")
        sys.exit(1)

    print(f"\nCollection: {info['name']}")
    print(f"Documents: {info['count']}")
    print("=" * 60)

    print("\n--- RAG Search Interface ---")
    print("Type your search query and press Enter.")
    print("Type 'quit' or 'exit' to exit.\n")

    while True:
        try:
            query = input("Search query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if query.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break

        if not query:
            continue

        results = searcher.search(query, top_k=3)

        if not results:
            print("No results found.\n")
            continue

        for result in results:
            print(f"\n--- Result {result['rank']} ---")
            print(f"Source: {result['metadata'].get('source', 'Unknown')}")
            score = result['score']
            if score is not None:
                similarity = 1 / (1 + score) * 100  # Convert distance to similarity %
                print(f"Relevance: {similarity:.2f}%")
            doc_preview = result['document'][:600]
            print(f"\n{doc_preview}...\n")


if __name__ == "__main__":
    main()
