from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

# ===============================
# CONFIG
# ===============================
API_KEY = "sk_test_123456789"

app = FastAPI(
    title="Agentic Honeypot API",
    description="Agentic Honeypot for Scam Detection & Intelligence Extraction",
    version="1.0"
)

# ===============================
# DATA MODELS
# ===============================
class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

# ===============================
# HEALTH CHECK (GET)
# Tester often sends GET first
# ===============================
@app.get("/api/honeypot")
def honeypot_health_check():
    return {
        "status": "alive",
        "message": "Honeypot endpoint is reachable"
    }

# ===============================
# MAIN HONEYPOT ENDPOINT (POST)
# ===============================
@app.post("/api/honeypot")
async def honeypot_endpoint(
    request: Request,
    payload: HoneypotRequest,
    x_api_key: Optional[str] = Header(None)
):
    # 🔐 API KEY VALIDATION (POST ONLY)
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    incoming_text = payload.message.text.lower()

    # 🧠 BASIC SCAM SIGNALS (starter logic)
    scam_keywords = [
        "block",
        "blocked",
        "verify",
        "urgent",
        "upi",
        "account",
        "suspended",
        "freeze",
        "bank"
    ]

    is_scam = any(word in incoming_text for word in scam_keywords)

    # 🎭 HUMAN-LIKE HONEYPOT RESPONSE
    if is_scam:
        reply = "What do you mean? I didn’t receive any official message about this."
    else:
        reply = "Sorry, I’m not sure I understand. Can you explain a bit more?"

    return {
        "status": "success",
        "reply": reply
    }
