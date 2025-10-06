from fastapi import APIRouter, Request
router = APIRouter()

# Simulated endpoints to emulate M-Pesa callbacks and STK push flow for testing.

@router.post('/stk_push')
async def stk_push(request: Request):
    payload = await request.json()
    # Example payload handling - in production Safaricom calls your callback
    return {"status": "received", "payload": payload}

@router.post('/callback')
async def mpesa_callback(request: Request):
    body = await request.json()
    # Process callback and update transaction status in database (left as exercise)
    # For demo return success
    return {"status": "ok", "received": body}
