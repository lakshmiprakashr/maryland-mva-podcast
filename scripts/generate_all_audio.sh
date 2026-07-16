#!/bin/bash
# Generate all audio files in background
# Usage: nohup ./generate_all_audio.sh &

set -e

cd "$(dirname "$0")/.."

echo "Starting full audio generation..."
echo "This will take approximately 30-45 minutes."
echo "Output will be logged to output/generation.log"
echo ""

# Run generation
uv run python scripts/generate_audio.py > output/generation.log 2>&1 &

PID=$!
echo "Generation started with PID: $PID"
echo "Monitor with: tail -f output/generation.log"
echo "Stop with: kill $PID"

echo $PID > output/generation.pid
