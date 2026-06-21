# RAG System with ChromaDB

A simple Retrieval-Augmented Generation (RAG) system using ChromaDB for semantic search.

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

## Setup

1. **Activate the virtual environment:**
   ```bash
   cd /Users/rezwan/Downloads/project1/RAG
   source .venv/bin/activate
   ```

2. **Install dependencies (if needed):**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Ingest Documents

Load all `.md` and `.json` files from the `doc/` directory into ChromaDB:

```bash
python ingest.py
```

### Search Documents

Start the interactive search interface:

```bash
python search.py
```

Then type your query. For example:
- "machine learning"
- "neural networks"  
- "transformers"
- "BERT"

Type `quit` or `exit` to close.

## How It Works

1. **Ingestion:** The system reads all markdown and JSON files, generates vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`, and stores them in ChromaDB.

2. **Search:** When you search for a query, it converts your query to an embedding and finds the most similar documents based on cosine similarity.

## Requirements

- Python 3.9+
- chromadb
- sentence-transformers
