# RAG System with ChromaDB

A simple Retrieval-Augmented Generation (RAG) system using ChromaDB for semantic search. Search through your documents using natural language queries.

## GitHub Repository

📦 https://github.com/rezwansys/project1-rag

## Quick Start

### From Scratch
```bash
# Clone the repository
git clone https://github.com/rezwansys/project1-rag.git
cd project1-rag/RAG

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ingest documents (run once)
python ingest.py

# Start searching!
python search.py
```

## Project Structure

```
RAG/
├── doc/                    # Document directory (.md and .json files)
│   ├── document1.md        # Machine Learning Overview
│   ├── document2.md        # Deep Learning Fundamentals
│   ├── document3.md        # Natural Language Processing
│   ├── config1.json        # RAG System Configuration
│   ├── config2.json        # API & Model Configuration
│   └── references.json     # Research Papers & Datasets
├── chroma_db/              # ChromaDB persistence (auto-created)
├── .venv/                  # Python virtual environment
├── ingest.py               # Ingestion script
├── search.py               # Search script
└── requirements.txt        # Dependencies
```

## Usage

### 1. Ingest Documents

Load all `.md` and `.json` files from the `doc/` directory into ChromaDB:

```bash
python ingest.py
```

Output:
```
============================================================
RAG Ingestion Script
============================================================
Starting ingestion...
Found 6 documents. Generating embeddings...
Successfully ingested 6 documents into ChromaDB.
Ingestion complete: 6 documents ingested
Failed: 0
============================================================
```

### 2. Search Documents

Start the interactive search interface:

```bash
python search.py
```

Then type your query. For example:
- "machine learning"
- "neural networks"  
- "transformers"
- "BERT"
- "What is supervised learning?"

Type `quit` or `exit` to close.

## Example Search Session

```
============================================================
RAG Search Script
============================================================

Collection: rag_documents
Documents: 6
============================================================

--- RAG Search Interface ---
Type your search query and press Enter.
Type 'quit' or 'exit' to exit.

Search query: machine learning

--- Result 1 ---
Source: doc/document1.md
Relevance: 53.45%

# Machine Learning Overview
Machine Learning (ML) is a subset of artificial intelligence...
```

## How It Works

### Ingestion Process
1. Reads all `.md` and `.json` files from the `doc/` directory
2. Generates vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`
3. Stores documents with metadata in ChromaDB

### Search Process  
1. Converts your query to an embedding
2. Finds the most similar documents based on cosine similarity
3. Returns results sorted by relevance score (converted to percentage)

## Configuration

You can customize the behavior by modifying the scripts:

- **Embedding Model**: Change in `ingest.py` and `search.py`:
  ```python
  self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
  ```

- **Top K Results**: Modify `top_k` parameter in search:
  ```python
  results = searcher.search(query, top_k=5)  # Default is 3
  ```

- **Persistence Directory**: Change where ChromaDB stores data:
  ```python
  ingestor = RAGIngestor(doc_dir="./doc", persist_dir="./chroma_db")
  ```

## Requirements

- Python 3.9+
- chromadb
- sentence-transformers

### Installation

```bash
pip install chromadb sentence-transformers
```

Or use the included `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Adding Your Own Documents

1. Create new `.md` or `.json` files in the `doc/` directory
2. Run `python ingest.py` to re-index all documents
3. Search using `python search.py`

## Troubleshooting

### "No documents found" error
Run `python ingest.py` first to create the ChromaDB database.

### Network errors during ingestion
The embedding model is downloaded from Hugging Face on first run. Ensure you have internet connectivity, or download the model separately.

### Empty search results
Try different keywords or verify that documents exist in the `doc/` directory and have been ingested.

## License

MIT License - Feel free to use and modify for your projects.
