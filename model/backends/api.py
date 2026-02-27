import os
import urllib.request
import json

class APIBackend:
    """OpenAI/Anthropic API backend"""
    
    def __init__(self, config: dict):
        self.provider = config.get("provider", "openai")
        self.model = config.get("model", "gpt-3.5-turbo")
        self.url = config.get("url", "https://api.openai.com/v1/chat/completions")
        
        # Prefer env var, fallback to config
        self.key = os.getenv("ELARA_API_KEY") or config.get("key", "")
        
        if not self.key:
            raise ValueError("API key not found. Set ELARA_API_KEY or config.model.api.key")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}"
        }
        
        if self.provider == "openai":
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are Elara, a helpful IT assistant."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
        
        req = urllib.request.Request(
            self.url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
                return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"API Error: {e}"