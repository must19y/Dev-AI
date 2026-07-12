#!/bin/sh

echo "Starting Ollama..."

ollama serve &

echo "Waiting for Ollama to become available..."

until ollama list >/dev/null 2>&1
do
    sleep 1
done

echo "Ollama is ready."

echo "Checking model..."

ollama pull llama3.2

echo "Model ready."

wait