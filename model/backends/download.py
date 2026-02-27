import os
import urllib.request
from .local import LocalBackend

class DownloadBackend:
    """Auto-download from HuggingFace then load locally"""
    
    HF_URL = "https://huggingface.co/{repo}/resolve/main/{file}"
    
    def __init__(self, config: dict):
        self.repo = config.get("repo")
        self.file = config.get("file")
        cache_dir = config.get("cache_dir", "models")
        
        if not self.repo or not self.file:
            raise ValueError("download.repo and download.file required in config")
        
        os.makedirs(cache_dir, exist_ok=True)
        self.model_path = os.path.join(cache_dir, self.file)
        
        # Download if not exists
        if not os.path.exists(self.model_path):
            self._download()
        
        # Load as local backend
        local_config = {"path": self.model_path, "threads": 4, "context_size": 4096}
        self.backend = LocalBackend(local_config)

    def _download(self):
        url = self.HF_URL.format(repo=self.repo, file=self.file)
        print(f"Downloading {self.file} from {self.repo}...")
        print(f"This may take several minutes...")
        
        urllib.request.urlretrieve(url, self.model_path)
        print(f"Downloaded to {self.model_path}")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        return self.backend.generate(prompt, max_tokens)