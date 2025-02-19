from fastapi import FastAPI, Header, HTTPException
import random

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from Mission Service!"}



@app.get("/validate")
async def validate(authorization: str = Header(None)):
    expected_token = "Bearer Agent007"
    if authorization != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
    
    missions = [
        {
            "mission_title": "Operation Silent Strike (But Actually Kinda Loud)",
            "mission_objective": "Gather Intelligence (and Maybe Snacks) on Target Organization",
            "mission_details": (
                "Agent, your mission, should you choose to accept it (and we really hope you do, we're short-staffed), "
                "involves infiltrating the enemy's secure facility (which probably has terrible coffee), obtaining classified "
                "documents (mostly recipes, we think), and exfiltrating without detection (or at least without tripping any alarms). "
                "Exercise extreme caution (especially around the vending machine) and follow established protocols (like 'don't spill coffee on the documents')."
            )
        },
        {
            "mission_title": "Project Nightingale (Because Doctors Are Cool)",
            "mission_objective": "Infiltrate enemy hospital (disguised as a very convincing potted plant)",
            "mission_details": (
                "Locate patient zero (who probably just has a cold) and retrieve the vial (of questionable origin). "
                "Try not to sneeze on anything important."
            )
        },
        {
            "mission_title": "Project Blackout (Because We Forgot to Pay the Electric Bill)",
            "mission_objective": "Disable the power grid (by unplugging the main reactor... just kidding... mostly)",
            "mission_details": (
                "Infiltrate the power plant (which smells vaguely of ozone and regret) and disable the main reactor (safely, please). "
                "Bring a flashlight. And maybe a sandwich."
            )
        }
    ]
    
    selected_mission = random.choice(missions)
    
    return {
        "status": "access_granted",
        "token": authorization.split(" ")[1],
        "message": f"Agent validated with token {authorization.split(' ')[1]}. Mission briefing is now available.",
        "mission_briefing": selected_mission
    }
