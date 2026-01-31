from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "sk_test_123456789"   # same key use karna

app = FastAPI(title="Agentic Honeypot API")

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[dict] = {}

@app.post("/api/honeypot")
def honeypot_endpoint(
    request: HoneypotRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    text = request.message.text.lower()
    scam_words = ["block", "verify", "urgent", "upi", "account", "suspended"]

    if any(w in text for w in scam_words):
        reply = "What do you mean? I did not receive any official message."
    else:
        reply = "Sorry, can you explain a bit more?"

    return {
        "status": "success",
        "reply": reply
    }
