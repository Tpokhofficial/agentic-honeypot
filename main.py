from fastapi import FastAPI

app = FastAPI()

# ROOT ENDPOINT — TESTER KE LIYE SABSE ZAROORI
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Honeypot service is running"
    }
