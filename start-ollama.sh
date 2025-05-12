#!/bin/bash

# Get model name from environment variable or use default
MODEL_NAME=${OLLAMA_MODEL:-"llama2:7b"}

# Start Ollama in the background with GPU support
OLLAMA_GPU_LAYERS=all ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
max_retries=30
retry_count=0

while [ $retry_count -lt $max_retries ]; do
    if ollama list > /dev/null 2>&1; then
        echo "Ollama service is ready"
        break
    fi
    echo "Waiting for Ollama service... (attempt $((retry_count + 1))/$max_retries)"
    sleep 2
    retry_count=$((retry_count + 1))
done

if [ $retry_count -eq $max_retries ]; then
    echo "Failed to connect to Ollama service"
    exit 1
fi

# Print current model list with more detail
echo "Current available models:"
ollama list
echo "Raw model list output:"
ollama list | cat

# Check if model exists using ollama list
echo "Checking for $MODEL_NAME model..."
if ! ollama list | grep -q "$MODEL_NAME"; then
    echo "Model not found in list, checking data directory..."
    if [ -d "/root/.ollama/models/$MODEL_NAME" ]; then
        echo "Model found in data directory but not in list. Attempting to load..."
        OLLAMA_GPU_LAYERS=all ollama pull "$MODEL_NAME"
    else
        echo "Model not found anywhere, pulling $MODEL_NAME..."
        OLLAMA_GPU_LAYERS=all ollama pull "$MODEL_NAME"
    fi
else
    echo "Model $MODEL_NAME is already installed"
fi

# Verify the model is loaded
echo "Verifying model is loaded..."
ollama list

# Keep the container running
wait 