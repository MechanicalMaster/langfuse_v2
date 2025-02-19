#!/bin/bash
export PORT="${PORT:-8000}"
uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 75 --log-level debug 