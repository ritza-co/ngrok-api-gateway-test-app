from fastapi import FastAPI, Header
from fastapi.responses import FileResponse
import httpx
import os

app = FastAPI()

@app.get("/", response_class=FileResponse)
async def homepage():
    # Serve the static HTML file.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "index.html")
    return FileResponse(file_path)

@app.get("/check_auth")
async def check_auth(authorization: str = Header(None)):
    # Send the token to the Auth Service.
    headers = {"Authorization": authorization}
    
    # Call the Auth Service using its Docker Compose hostname.
    async with httpx.AsyncClient() as client:
        response = await client.get("http://mission-service:5001/validate", headers=headers)
    auth_response = response.json()
    
    # Format the mission briefing with structured details.
    mission_briefing = auth_response
    
    return mission_briefing

