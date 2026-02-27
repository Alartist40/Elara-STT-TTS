from .local import LocalBackend
from .api import APIBackend
from .ollama import OllamaBackend
from .download import DownloadBackend

BACKENDS = {
    "local": LocalBackend,
    "api": APIBackend,
    "ollama": OllamaBackend,
    "download": DownloadBackend,
}