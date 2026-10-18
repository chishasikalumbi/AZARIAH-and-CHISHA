import os
import sys

# Ensure the 'src' directory is in Python's search path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from generate import generate_answer

def run_chatbot():
    print("==================================================")
    print("  PURE PYTHON COMPUTER SCIENCE TEXTBOOK RAG BOT  ")
    print("==================================================")
    print("Type your question below (or type 'exit' / 'quit' to stop).\n")

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("\nExiting chatbot session. Goodbye!")
                break
                
            print("\nSearching textbooks and generating response...\n")
            print("-" * 50)
            generate_answer(user_input, top_k=3)
            print("-" * 50)
            print("\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Goodbye!")
            break

if __name__ == "__main__":
    run_chatbot()