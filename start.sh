#!/bin/bash

set -e

echo "Starting Data Analyzer on port 5001..."

gunicorn applications.data_analyzer_server.app:app \
    --bind 127.0.0.1:5001 \
    --workers 1 &

ANALYZER_PID=$!

cleanup() {
    kill "$ANALYZER_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

echo "Starting Smart Planner web server on port $PORT..."

gunicorn applications.basic_server.app:app \
    --bind 0.0.0.0:"$PORT" \
    --workers 1
