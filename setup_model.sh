#!/bin/bash

# Define the URL and the target directory
MODEL_URL="https://huggingface.co/ggml-org/gemma-1.1-7b-it-Q4_K_M-GGUF/resolve/main/gemma-1.1-7b-it.Q4_K_M.gguf?download=true"
TARGET_DIR="./llama.cpp/models"

# Create the target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Download the model
echo "Downloading the model..."
curl -L -o "$TARGET_DIR/gemma-1.1-7b-it.Q4_K_M.gguf" "$MODEL_URL"

echo "Model downloaded and saved to $TARGET_DIR"