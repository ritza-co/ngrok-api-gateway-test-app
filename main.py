import requests
import time

# Replace with your actual Kong Konnect details
KONNECT_ADMIN_API = "https://us.api.konghq.com/v2/control-planes/e9603566-65b6-46d8-a9b7-18637b1888e5"
KONNECT_ADMIN_TOKEN = "kpat_D49Sd7j0gv7yR5tfAIUpROI64E3Z7sh6rT9tNhhJ1G9gxYjlB"

HEADERS = {
    "Authorization": f"Bearer {KONNECT_ADMIN_TOKEN}",
    "Content-Type": "application/json"
}

SERVICES = [
    {
        "name": "auth-service",
        "url": "http://auth-service:5001",
        "route": "/auth",
        "rate_limit": 20  # requests per minute
    },
    {
        "name": "agent-portal",
        "url": "http://agent-portal:5002",
        "route": "/agent-portal",
        "rate_limit": 50  # requests per minute
    }
]

def register_service(service):
    """Registers a service in Kong Konnect."""
    url = f"{KONNECT_ADMIN_API}/services/"
    data = {"name": service["name"], "url": service["url"]}
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Registering {service['name']}: {response.status_code}")
    return response.status_code == 201 or response.status_code == 200

def create_route(service):
    """Creates a route for a service."""
    url = f"{KONNECT_ADMIN_API}/services/{service['name']}/routes"
    data = {"paths": [service["route"]]}
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Creating route for {service['name']}: {response.status_code}")
    return response.status_code == 201 or response.status_code == 200

def apply_rate_limit(service):
    """Applies rate limiting to a service."""
    url = f"{KONNECT_ADMIN_API}/services/{service['name']}/plugins"
    data = {
        "name": "rate-limiting",
        "config": {"minute": service["rate_limit"]}
    }
    response = requests.post(url, json=data, headers=HEADERS)
    print(f"Applying rate limit for {service['name']}: {response.status_code}")
    return response.status_code == 201 or response.status_code == 200

def test_service(service):
    """Tests the service endpoint."""
    url = f"{KONNECT_ADMIN_API}{service['route']}"
    print(f"Testing {service['name']} at {url}...")
    response = requests.get(url)
    print(f"Response: {response.status_code} - {response.text}")

def main():
    """Automates the Kong Konnect setup."""
    for service in SERVICES:
        register_service(service)
        time.sleep(2)
        create_route(service)
        time.sleep(2)
        apply_rate_limit(service)
        time.sleep(2)
    
    print("\n✅ Setup complete! Testing services...\n")
    for service in SERVICES:
        test_service(service)

if __name__ == "__main__":
    main()


    main()

    