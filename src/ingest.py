import os
import json
import math
from collections import Counter
import re

def tokenize(text):
    """Simple helper to split text into lowercase words."""
    return re.findall(r'\b\w+\b', text.lower())

def build_pure_python_index():
    # Automatically locate paths relative to the project root folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    passages_path = os.path.join(base_dir, "artifacts", "passages.json")
    output_path = os.path.join(base_dir, "artifacts", "pure_python_index.json")

    print(f"Loading passages from {passages_path}...")
    with open(passages_path, "r", encoding="utf-8") as f:
        passages = json.load(f)
        
    print(f"Building pure Python search index for {len(passages)} passages...")
import os
import json
import pypdf

def load_manifest():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base_dir, "data", "book_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

def ingest_books():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    output_path = os.path.join(base_dir, "artifacts", "passages.json")
    
    manifest = load_manifest()
    all_chunks = []
    
    # Loop through books listed in book_manifest.json
    for book in manifest.get("books", []):
        filename = book.get("filename")
        pdf_path = os.path.join(data_dir, filename)
        if not os.path.exists(pdf_path):
            print(f"Warning: {pdf_path} not found.")
            continue
            
        print(f"Processing: {book.get('title', filename)}...")
        reader = pypdf.PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                all_chunks.append({
                    "text": text.strip(),
                    "source": book.get("title", filename),
                    "page": page_num + 1
                })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
    print(f"Success! Saved passages to {output_path}")

if __name__ == "__main__":
    ingest_books()