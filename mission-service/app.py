from fastapi import FastAPI, Header, HTTPException
import random

app = FastAPI()

# predefined missions for different agents
AGENT_MISSIONS = {
    "Agent007": [
        {
            "mission_title": "Operation Silent Strike (But Actually Kinda Loud)",
            "mission_objective": "Gather Intelligence (and Maybe Snacks) on Target Organization",
            "mission_details": (
                "Agent, your mission, should you choose to accept it (and we really hope you do, we're short-staffed), "
                "involves infiltrating the enemy's secure facility (which probably has terrible coffee), obtaining classified "
                "documents (mostly recipes, we think), and exfiltrating without detection (or at least without tripping any alarms). "
                "Exercise extreme caution (especially around the vending machine) and follow established protocols (like 'don't spill coffee on the documents')."
            ),
        },
        {
            "mission_title": "Project Nightingale (Because Doctors Are Cool)",
            "mission_objective": "Infiltrate enemy hospital (disguised as a very convincing potted plant)",
            "mission_details": (
                "Locate patient zero (who probably just has a cold) and retrieve the vial (of questionable origin). "
                "Try not to sneeze on anything important."
            ),
        },
    ],
    "AgentX": [
        {
            "mission_title": "Operation Red Storm",
            "mission_objective": "Neutralize rogue AI in top-secret facility",
            "mission_details": (
                "Agent, your mission is to infiltrate an underground AI research facility. The AI has gone rogue, and your job is to shut it down. "
                "Avoid security bots, retrieve critical data, and ensure the AI doesn’t escape to the cloud. Also, don’t let it talk you into anything—it’s very persuasive."
            ),
        },
        {
            "mission_title": "Project Eclipse",
            "mission_objective": "Steal classified technology from enemy base",
            "mission_details": (
                "Your target is an advanced quantum computing chip developed by a rival agency. Expect heavy security, infrared sensors, "
                "and at least one really bored guard playing on his phone. Get in, grab the chip, and get out without triggering international incidents."
            ),
        },
    ],
    "Agent99": [
        {
            "mission_title": "Operation Midnight Sun",
            "mission_objective": "Sabotage enemy communications before dawn",
            "mission_details": (
                "You have until sunrise to disable the enemy’s satellite uplink. It’s somewhere in a remote mountain base. Expect snow, guard dogs, and a lot of hiking. "
                "Also, bring hot cocoa—it's cold as hell up there."
            ),
        }
    ]
}

def extract_agent_id(authorization: str) -> str:
    """Extracts agent ID from the Bearer token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token format")
    
    agent_id = authorization.split(" ")[1]  # Extracts the agent ID
    return agent_id

@app.get("/")
async def read_root():
    return {"message": "Hello from Mission Service!"}

@app.get("/validate")
async def validate(authorization: str = Header(None)):
    agent_id = extract_agent_id(authorization)

    if agent_id not in AGENT_MISSIONS:
        raise HTTPException(status_code=403, detail="Unauthorized: No missions assigned to this agent")

    mission = random.choice(AGENT_MISSIONS[agent_id])

    return {
        "status": "access_granted",
        "agent": agent_id,
        "message": f"Agent {agent_id} validated. Your mission briefing is now available.",
        "mission_briefing": mission
    }