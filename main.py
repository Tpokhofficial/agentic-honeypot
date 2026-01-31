from fastapi import FastAPI, Response

app = FastAPI()

def ok_response():
    return {
        "status": "ok",
        "message": "Honeypot service is running"
    }

# Allow GET
@app.get("/")
def root_get():
    return ok_response()

# Allow POST
@app.post("/")
def root_post():
    return ok_response()

# Allow HEAD
@app.head("/")
def root_head(response: Response):
    response.status_code = 200
    return response

# Allow OPTIONS (important for testers)
@app.options("/")
def root_options(response: Response):
    response.status_code = 200
    return response

# Catch-all for any path + any method
@app.api_route("/{path:path}", methods=["GET", "POST", "HEAD", "OPTIONS"])
def catch_all(path: str, response: Response):
    response.status_code = 200
    return ok_response()
