#!/usr/bin/env bash
# Run the FastAPI app (example)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
