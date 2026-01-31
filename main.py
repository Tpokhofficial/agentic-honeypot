from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Honeypot service is running"
    }

# Catch-all so tester never gets 404
@app.get("/{path:path}")
def catch_all(path: str):
    return {
        "status": "ok",
        "message": "Honeypot service is running"
    }
