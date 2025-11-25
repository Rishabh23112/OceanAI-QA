#!/bin/sh
set -e

BACKEND_PORT="${BACKEND_PORT:-8000}"
PORT="${PORT:-8501}"

# Ensure the Streamlit app talks to the local FastAPI instance by default.
export BACKEND_URL="${BACKEND_URL:-http://127.0.0.1:${BACKEND_PORT}}"

uvicorn backend.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" &
UVICORN_PID=$!

cleanup() {
  echo "Stopping backend (pid: ${UVICORN_PID})"
  kill "${UVICORN_PID}"
  wait "${UVICORN_PID}"
}

trap cleanup INT TERM

echo "Starting Streamlit UI on port ${PORT}"
streamlit run frontend/app.py --server.port "${PORT}" --server.address 0.0.0.0

cleanup

