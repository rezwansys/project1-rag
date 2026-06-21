#!/usr/bin/env python3
"""
RAG Ingestion Script
Ingests .md and .json files from the doc directory into ChromaDB for semantic search.
"""

import json
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict, Any


class RAGIngestor:
    """Handles ingestion of documents into ChromaDB."""

    def __init__(self, doc_dir: str = "./doc", persist_dir: str = "./chroma_db"):
        self.doc_dir = Path(doc_dir)
        self.persist_dir = Path(persist_dir)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = self.client.get_or_create_collection(
            name="rag_documents",
            metadata={"description": "RAG documents for semantic search"}
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def extract_text_from_md(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_text_from_json(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, indent=2)

    def get_documents(self) -> List[Dict[str, Any]]:
        documents = []
        for ext in ['*.md', '*.json']:
            for file_path in self.doc_dir.glob(ext):
                try:
                    if ext == '*.md':
                        text = self.extract_text_from_md(file_path)
                    else:
                        text = self.extract_text_from_json(file_path)

                    documents.append({
                        "id": file_path.stem,
                        "text": text,
                        "source": str(file_path),
                        "type": ext
                    })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
        return documents

    def ingest(self) -> Dict[str, int]:
        print("Starting ingestion...")
        documents = self.get_documents()

        if not documents:
            print("No documents found to ingest.")
            return {"ingested": 0, "failed": 0}

        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = [{"source": doc["source"], "type": doc["type"]} for doc in documents]

        print(f"Found {len(documents)} documents. Generating embeddings...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True).tolist()

        # Clear existing collection and add new documents
        self.client.delete_collection("rag_documents")
        self.collection = self.client.get_or_create_collection(
            name="rag_documents",
            metadata={"description": "RAG documents for semantic search"}
        )

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )

        print(f"Successfully ingested {len(documents)} documents into ChromaDB.")
        return {"ingested": len(documents), "failed": 0}


def main():
    print("=" * 60)
    print("RAG Ingestion Script")
    print("=" * 60)

    ingestor = RAGIngestor(
        doc_dir="./doc",
        persist_dir="./chroma_db"
    )

    result = ingestor.ingest()
    print(f"\nIngestion complete: {result['ingested']} documents ingested")
    print(f"Failed: {result['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
