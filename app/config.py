import os

# Model configuration
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama2:7b")
 
# Ollama service configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434") 