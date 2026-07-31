# test_ollama_simple.py
import ollama
import json

def test_ollama():
    """Simple test to verify Ollama and Qwen are working"""
    print("Testing Ollama with Qwen2.5...")
    
    try:
        response = ollama.chat(
            model='qwen2.5:3b-instruct',
            messages=[
                {"role": "user", "content": "What is 2+2? Return only JSON: {\"answer\": 4}"}
            ],
            format='json'
        )
        
        print(f"Response: {response['message']['content']}")
        print("✅ Ollama is working!")
        return True
        
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        print("\nMake sure Ollama is running and the model is pulled:")
        print("  ollama serve")
        print("  ollama pull qwen2.5:3b-instruct")
        return False

if __name__ == "__main__":
    test_ollama()