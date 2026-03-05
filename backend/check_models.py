import ollama
from sentence_transformers import SentenceTransformer

def main():
    print("Checking Ollama...")
    try:
        models = ollama.list()
        # ollama.list() usually returns an object or a dict.
        # It's an object `ollama.ListResponse` in newer versions.
        model_names = [m.model for m in models.models]
        if any('qwen2.5:7b' in m or 'qwen2.5' in m for m in model_names):
            print("OK: qwen2.5 is installed.", model_names)
        else:
            print("MISSING: qwen2.5 is not installed.", model_names)
    except Exception as e:
        print("Error checking ollama:", e)
        
    print("Checking SentenceTransformer...")
    try:
        # This will download it if not present, but let's see if it works
        model = SentenceTransformer("BAAI/bge-small-en")
        print("OK: BAAI/bge-small-en is loaded successfully.")
    except Exception as e:
        print("Error loading SentenceTransformer:", e)

if __name__ == "__main__":
    main()
