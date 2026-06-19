#!/bin/sh
set -e

echo "Waiting for Qdrant..."
until curl -s http://qdrant:6333/collections > /dev/null 2>&1; do
  sleep 2
done
echo "Qdrant is ready."

echo "Checking if collection exists..."
if curl -s -o /dev/null -w "%{http_code}" http://qdrant:6333/collections/learning-RAG | grep -q "^2"; then
  echo "Collection already exists."
else
  echo "Creating collection via index.py..."
  python index.py && echo "Collection created." || echo "index.py failed (may already exist)."
fi

echo "Starting uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
