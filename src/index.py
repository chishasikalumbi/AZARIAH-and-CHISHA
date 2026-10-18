import os
import json
import re
import math
from collections import Counter, defaultdict

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_pure_python_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    passages_path = os.path.join(base_dir, "artifacts", "passages.json")
    output_path = os.path.join(base_dir, "artifacts", "pure_python_index.json")
    
    print(f"Loading passages from {passages_path}...")
    with open(passages_path, "r", encoding="utf-8") as f:
        passages = json.load(f)
        
    print(f"Building pure Python search index for {len(passages)} passages...")
    
    N = len(passages)
    df = Counter()
    doc_term_freqs = []
    
    for passage in passages:
        tokens = tokenize(passage.get("text", ""))
        tf = Counter(tokens)
        doc_term_freqs.append(tf)
        for term in tf.keys():
            df[term] += 1
            
    # Compute IDF
    idf = {}
    for term, freq in df.items():
        idf[term] = math.log(1 + (N / freq))
        
    # Compute normalized TF-IDF vector for each document
    doc_vectors = []
    for tf in doc_term_freqs:
        doc_vec = {}
        norm = 0.0
        for term, count in tf.items():
            if term in idf:
                val = count * idf[term]
                doc_vec[term] = val
                norm += val ** 2
        doc_vectors.append(doc_vec)
        
    index_data = {
        "passages": passages,
        "idf": idf,
        "doc_vectors": doc_vectors
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False)
        
    print(f"Success! Pure Python index saved to {output_path}.")

if __name__ == "__main__":
    build_pure_python_index()