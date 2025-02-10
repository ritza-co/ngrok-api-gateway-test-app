from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from Auth Service!"}



@app.get("/validate")
async def validate(authorization: str = Header(None)):
    expected_token = "Bearer Agent007"
    if authorization != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    
    return {
        "status": "access_granted",
        "token": "Agent007",
        "message": "Agent validated. Mission briefing is now available."
    }