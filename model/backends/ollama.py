import urllib.request
import json

class OllamaBackend:
    """Local Ollama HTTP backend"""
    
    def __init__(self, config: dict):
        self.url = config.get("url", "http://localhost:11434/api/generate")
        self.model = config.get("model", "llama2")
        
        # Test connection
        try:
            urllib.request.urlopen("http://localhost:11434", timeout=2)
        except:
            raise ConnectionError("Ollama not running on localhost:11434")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        data = {
            "model": self.model,
            "prompt": f"You are Elara, an IT assistant. {prompt}",
            "stream": False,
            "options": {"num_predict": max_tokens}
        }
        
        req = urllib.request.Request(
            self.url,
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode())
                return result["response"].strip()
        except Exception as e:
            return f"Ollama Error: {e}"