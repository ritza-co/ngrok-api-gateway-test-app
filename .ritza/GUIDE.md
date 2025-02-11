# Setting Up ngrok as an API gateway

In this guide, we'll set up an ngrok agent as an API gateway to expose multiple services running on Docker containers. 

We'll also show how to add basic authentication using ngrok's traffic policies.

## The setup

This is a basic setup with two services: `auth-service` and `agent-portal`.

![](./assets/diagram.png)

The `agent-portal` service contains a really simple frontend that makes a request to the `auth-service` for authentication and fetches a secret message for James Bond.

The `auth-service` should ideally have some traffic policies in place to ensure only authenticated requests are allowed. In this example, we'll add basic authentication using ngrok's traffic policies to add a username and password. This way, the `agent-portal` service can freely make requests to the `auth-service` without worrying about authentication, while any external requests will need to provide the correct credentials.


## 1. Sign Up and Get an ngrok API Key

1. Go to ngrok.com and sign up
2. Navigate to the "Authtokens" section in the ngrok dashboard
3. Copy your Authtoken

## 2. Install the ngrok agent

### On macOS (Homebrew):
```bash
brew install ngrok
```

Next we can authenticate ngrok (not entirely necessary since we'll use a config file but helpful for testing locally):

```bash
ngrok config add-authtoken <YOUR_NGROK_AUTH_TOKEN>
```

## 3. Clone the repository

Next, clone the repository and checkout the `ngrok-agent` branch:

```bash
git clone <this-repo-url> 

cd api-gateway-test

git checkout ngrok-agent
```



## 4. Create ngrok.yml

Create a `ngrok` directory in the root of the project and add an `ngrok.yml` file with the following configuration:

```yaml
version: "3"
agent:
  authtoken: "YOUR_NGROK_AUTH_TOKEN"

endpoints:
  - name: auth-endpoint
    upstream:
      url: http://auth:5001
    traffic_policy:
      on_http_request:
        - actions:
            - type: basic-auth
              config:
                credentials:
                  - "admin:super-secret-password"

  - name: agent-portal-endpoint
    upstream:
      url: http://agent-portal:5002
```

This configuration sets up two endpoints: `auth-endpoint` and `agent-portal-endpoint`. The `auth-endpoint` has an authentication policy in place.

Our ngrok agent can use this configuration on startup.


## 5. Modify docker-compose.yml

We'll add an ngrok agent service to our `docker-compose.yml` file. We'll also add a network to allow the services to communicate with each other and we'll add the config file for the ngrok agent as a volume.

This service will forward traffic to our auth and agent-portal services. 

```yaml
version: '3.8'

services:
  auth:
    build: ./auth-service
    ports:
      - "5001:5001"

  agent-portal:
    build: ./agent-portal
    ports:
      - "5002:5002"

  ngrok:
    image: ngrok/ngrok:latest 
    command: "start --all --config /etc/ngrok/ngrok.yml"
    volumes:
      - ./ngrok/ngrok.yml:/etc/ngrok/ngrok.yml
    depends_on:
      - auth
      - agent-portal
    ports:
      - "443:443"
      - "4040:4040"
```

## 6. Start Services

Start the services using Docker Compose:

```bash
docker-compose up --build
```

List running containers to verify that the services are running:

```bash
docker ps
```

![](./assets/docker-verify.png)


## Check ngrok Dashboard

Visit your ngrok dashboard to see the endpoints and inspect the traffic policies.

![Dashboard](./assets/dashboard.png)

Clicking on the endpoint that corresponds to the agent portal should show our agent portal:

![Agent Portal](./assets/agent-portal.png)

Clicking on the endpoint that corresponds to the auth service should show the traffic policy:

![Traffic policy](./assets/auth-traffic-policy.png)

And we can verfy this by going to the auth-service endpoint:

![](./assets/auth-service-sign-in.png)

Enter the credentials and you should see the auth hello message:

![](./assets/hello-from-auth-service.png)
