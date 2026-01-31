from fastapi import FastAPI, Header, HTTPException
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
# HEALTH / TEST ROUTE (GET)
# ===============================
@app.get("/api/honeypot")
def honeypot_health_check():
    """
    This route exists ONLY to avoid 404 errors
    when testers send a GET request.
    """
    return {
        "status": "alive",
        "message": "Honeypot endpoint is reachable"
    }

# ===============================
# MAIN HONEYPOT LOGIC (POST)
# ===============================
@app.post("/api/honeypot")
def honeypot_endpoint(
    request: HoneypotRequest,
    x_api_key: str = Header(None)
):
    # 🔐 API KEY VALIDATION
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    incoming_text = request.message.text.lower()

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

    # 🎭 HUMAN-LIKE HONEYPOT REPLY
    if is_scam:
        reply = "What do you mean? I didn’t get any official message about this."
    else:
        reply = "Sorry, I’m not sure I understand. Can you explain?"

    return {
        "status": "success",
        "reply": reply
    }
