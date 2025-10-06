# Safaricom-style System (Pure Python) - Scaffold
This repository is a **pure Python** scaffold for a Safaricom-like company system with:
- FastAPI backend (REST + server-rendered templates)
- Simulated USSD endpoints
- Payments simulation (M-Pesa STK Push simulation hook)
- Simple AI Fraud Detector (rule-based + a pluggable ML model interface)
- SQLite database (SQLAlchemy)
- Basic dashboard templates with a modern background image
- Instructions to run locally (PyCharm friendly)

## What's included
- `app/main.py` — FastAPI application with endpoints and server-rendered pages
- `app/models.py` — SQLAlchemy models and DB setup
- `app/fraud.py` — Fraud detection module (rule-based + ML stub)
- `app/sim_mpesa.py` — Simulated M-Pesa STK Push endpoints
- `templates/` — Jinja2 HTML templates (dashboard, login, fraud monitor)
- `static/style.css` — Basic styling including background image
- `requirements.txt` — Python packages to install
- `run.sh` — Example run command

## Quick start (local)
1. Create virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Open `http://127.0.0.1:8000` in your browser.

## Notes
- This scaffold uses a simulated M-Pesa flow for development. Replace `app/sim_mpesa.py` with real provider integration when you obtain credentials.
- The AI fraud detector provides a rule-based detector and a clear place to plug in a trained ML model (joblib/pickle).
- The HTML templates reference a modern background image hosted on Unsplash. Replace with your preferred image or host locally.
