import os
import json
import re
import math
from collections import Counter

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def generate_answer(query, top_k=3):
    # Locate paths relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, "artifacts", "pure_python_index.json")
    
    if not os.path.exists(index_path):
        print(f"Error: Index file not found at {index_path}. Run index.py first.")
        return
        
    print(f"Loading search index for RAG generation...")
    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)
        
    passages = index_data.get("passages", [])
    idf = index_data.get("idf", {})
    doc_vectors = index_data.get("doc_vectors", [])
    
    if not passages:
        print("Index is empty.")
        return

    # Process and vectorize query
    query_tokens = tokenize(query)
    query_tf = Counter(query_tokens)
    
    query_vector = {}
    query_norm = 0.0
    for term, count in query_tf.items():
        if term in idf:
            weight = count * idf[term]
            query_vector[term] = weight
            query_norm += weight ** 2
            
    query_norm = math.sqrt(query_norm)
    
    if query_norm == 0.0:
        print("No matching terms found in query vocabulary.")
        return

    # Compute cosine similarity
    scores = []
    for doc_idx, doc_vec in enumerate(doc_vectors):
        dot_product = 0.0
        doc_norm = 0.0
        for term, val in doc_vec.items():
            doc_norm += val ** 2
            if term in query_vector:
                dot_product += query_vector[term] * val
                
        doc_norm = math.sqrt(doc_norm)
        score = (dot_product / (query_norm * doc_norm)) if doc_norm > 0 else 0.0
        scores.append((score, doc_idx))
        
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Gather top passages for context
    context_passages = []
    for rank, (score, doc_idx) in enumerate(scores[:top_k], 1):
        if score == 0.0:
            break
        p = passages[doc_idx]
        context_passages.append(
            f"--- Excerpt {rank} (Source: {p.get('source')}, Page {p.get('page')}) ---\n{p.get('text')}"
        )
        
    context_str = "\n\n".join(context_passages)
    
    # Construct the final RAG prompt packet
    rag_prompt = f"""========================================
RAG PROMPT CONTEXT GENERATED SUCCESSFULLY
========================================

[System Role]
You are an intelligent Computer Science chatbot assistant. Answer the user's question using only the provided textbook context below.

[Retrieved Context Excerpts]
{context_str}

[User Question]
{query}
"""
    
    print(rag_prompt)
    return rag_prompt

if __name__ == "__main__":
    # Test query for generation
    user_query = "java"
    generate_answer(user_query, top_k=2)