# Pure Python RAG Chatbot for Computer Science Textbooks

A lightweight, zero-dependency Retrieval-Augmented Generation (RAG) chatbot built entirely in pure Python for querying Computer Science textbooks.

## Project Structure
- data/: Source PDF textbooks.
- artifacts/: Generated search indexes, extracted passages, and evaluation reports.
- src/: Core pipeline logic:
  - ingest.py: Parses PDFs into structured text passages.
  - index.py: Builds a pure-Python TF-IDF vocabulary and document vector index.
  - retrieve.py: Computes cosine similarity to retrieve relevant passages.
  - generate.py: Constructs clean RAG prompt contexts.
  - app.py: Interactive CLI interface for live chatting.
- evaluation/: Automated benchmark suite (evaluate.py).

## How to Run

1. *Build/Rebuild the Index*:
   ```bash
   python src/index.py