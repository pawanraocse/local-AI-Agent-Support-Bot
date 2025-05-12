import requests
import time
from config import OLLAMA_HOST, MODEL_NAME

def wait_for_ollama():
    """Wait for Ollama service to be ready and model to be available"""
    max_retries = 30  # 2.5 minutes total with 5-second intervals
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                for model in models:
                    if model.get('name') == MODEL_NAME:
                        print(f"Model {MODEL_NAME} is ready!")
                        return True
                print(f"Waiting for {MODEL_NAME} model to be available... (attempt {retry_count + 1}/{max_retries})")
            time.sleep(5)
            retry_count += 1
        except requests.exceptions.ConnectionError:
            print(f"Waiting for Ollama service to start... (attempt {retry_count + 1}/{max_retries})")
            time.sleep(5)
            retry_count += 1
    
    print("Failed to connect to Ollama service or model not available after maximum retries")
    return False

if __name__ == "__main__":
    if not wait_for_ollama():
        print("Failed to initialize Ollama service")
        exit(1)
    
    print("Initialization completed successfully!") 