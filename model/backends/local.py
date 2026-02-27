import os
from llama_cpp import Llama
from typing import Dict, Any, Optional

class LocalBackend:
    """Direct inference with quantized GGUF via llama.cpp"""
    
    def __init__(self, config: dict):
        model_path = config.get("path", "models/model.gguf")
        n_threads = config.get("threads", 4)
        n_ctx = config.get("context_size", 4096)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=0,
            chat_format="chatml",
            verbose=False,
        )
        
        self.system_prompt = """You are Elara, a helpful AI assistant.
Be concise, accurate, and helpful. If unsure, say so."""

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        output = self.model.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
            stop=["User:", "Assistant:"],
        )
        
        return output["choices"][0]["message"]["content"].strip()