from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from . import models, fraud, sim_mpesa
import os

app = FastAPI(title="Safaricom-style System (Pure Python)")
app.add_middleware(SessionMiddleware, secret_key='CHANGE_ME_TO_RANDOM')

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "static")), name="static")

# Initialize DB (SQLite)
models.init_db()

# Home / Dashboard
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = {
        "total_customers": models.count_customers(),
        "total_transactions": models.count_transactions(),
        "flagged_frauds": models.count_flagged(),
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats})

# Simple login (dev use)
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    # for demo: accept any username/password
    request.session['user'] = username
    return JSONResponse({"ok": True, "username": username})

# Example API endpoints
@app.post("/api/payments/charge")
async def charge_payment(payload: dict):
    # payload expects: customer_id, amount, method, device_id, ip_address
    fraud_resp = fraud.check_transaction(payload)
    # store transaction
    tx = models.create_transaction(payload, fraud_resp)
    return {"transaction": tx, "fraud": fraud_resp}

@app.post("/api/fraud/check")
async def api_fraud_check(payload: dict):
    resp = fraud.check_transaction(payload)
    return resp

# USSD simulation endpoint (for providers like Africa's Talking)
@app.post("/api/ussd")
async def ussd_endpoint(payload: dict):
    # simplistic USSD processing for demo
    session_id = payload.get("sessionId")
    text = payload.get("text", "")
    phone = payload.get("phoneNumber")
    if text == "":
        # show main menu
        return {"message": "CON Karibu\n1. Angalia Salio\n2. Lipa Bili\n3. Fungua Ticket"}
    if text == "1":
        # return balance
        bal = models.get_balance_by_msisdn(phone)
        return {"message": f"END Salio lako ni KSh {bal}"}
    if text.startswith("2"):
        # simulate pay flow
        return {"message": "CON Ingiza namba ya invoice:"}
    return {"message": "END Samahani, chaguo sio sahihi."}

# Include simulated M-Pesa callbacks
app.include_router(sim_mpesa.router, prefix="/sim_mpesa")
