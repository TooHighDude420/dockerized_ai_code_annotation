#!/bin/bash
set -e

echo "Starting Ollama server in background..."
ollama serve &  # start the server
SERVER_PID=$!

# Wait a few seconds for server to be ready
echo "Waiting for Ollama server to be ready..."
sleep 5  # adjust if needed

# Pull model only if missing
if ! ollama list | grep -q "codellama:7b"; then
    echo "Pulling codellama:7b model..."
    ollama pull codellama:7b
fi

echo "Ollama server is ready. Press Ctrl+C to stop."

# Keep container alive by tailing logs or waiting
wait $SERVER_PID