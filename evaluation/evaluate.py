import os
import sys
import json

# Add 'src' directory to module path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

from generate import generate_answer

def run_evaluation():
    print("==================================================")
    print("      RUNNING RAG SYSTEM EVALUATION BENCHMARK      ")
    print("==================================================")

    # Benchmark test questions
    test_questions = [
        "What is computer science?",
        "Explain data structures and algorithms.",
        "How does object oriented programming work in Java?",
        "What is relational database design?"
    ]

    results = []

    for idx, question in enumerate(test_questions, 1):
        print(f"\n[Test {idx}/{len(test_questions)}] Query: '{question}'")
        print("-" * 50)
        
        # Run generation pipeline
        prompt_output = generate_answer(question, top_k=2)
        
        results.append({
            "question_id": idx,
            "question": question,
            "generated_prompt_length": len(prompt_output) if prompt_output else 0,
            "status": "SUCCESS" if prompt_output else "FAILED"
        })

    # Save benchmark evaluation report
    report_path = os.path.join(base_dir, "artifacts", "evaluation_results.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\n==================================================")
    print(f"Evaluation complete! Summary saved to:\n{report_path}")
    print("==================================================")

if __name__ == "__main__":
    run_evaluation()