# Lesson 4: Agent Deployment with Azure AI Foundry Hosted Agents + ChatKit

This lesson demonstrates how to deploy a multi-agent workflow to Azure AI Foundry as a hosted agent and create a ChatKit-based frontend to interact with it.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User's Browser                               │
│                    (ChatKit React Frontend)                          │
│                      localhost:3000                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTP/SSE
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ChatKit Backend Server                           │
│                    (FastAPI + SQLite Store)                          │
│                      localhost:8001                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ Azure AI Responses API
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry                                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │               Hosted Multi-Agent Workflow                      │  │
│  │  ┌─────────────┐  ┌──────────────────┐  ┌───────────────┐     │  │
│  │  │   Triage    │──│ Employee Search  │  │   Learning    │     │  │
│  │  │   Agent     │  │     Agent        │  │    Agent      │     │  │
│  │  │(Coordinator)│  │ (Vector Store)   │  │ (MCP Tool)    │     │  │
│  │  └──────┬──────┘  └──────────────────┘  └───────────────┘     │  │
│  │         │         ┌──────────────────┐                         │  │
│  │         └─────────│  Coding Agent    │                         │  │
│  │                   │ (Code Generation)│                         │  │
│  │                   └──────────────────┘                         │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. **Azure AI Foundry Project** in North Central US region
2. **Azure CLI** authenticated (`az login`)
3. **Azure Developer CLI** (`azd`) installed
4. **Python 3.12+** and **Node.js 18+**
5. **Vector Store** created with employee data

## Quick Start

### 1. Set Up Environment Variables

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edit .env with your Azure AI Foundry project details
```

### 2. Deploy the Hosted Agent

**Option A: Using Azure Developer CLI (Recommended)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Option B: Using Docker + Azure Container Registry**

```bash
cd hosted-agent

# Build the container
docker build -t developer-onboarding-agent:latest .

# Tag for ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Push to ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Deploy via Azure AI Foundry portal or SDK
```

### 3. Start the ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server will start on `http://localhost:8001`

### 4. Start the ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`

### 5. Test the Application

Open `http://localhost:3000` in your browser and try these queries:

**Employee Search:**
- "I'm new here! Has anyone worked at Microsoft?"
- "Who has experience with Azure Functions?"

**Learning Resources:**
- "Create a learning path for Kubernetes"
- "What certifications should I pursue for cloud architecture?"

**Coding Help:**
- "Help me write Python code for connecting to CosmosDB"
- "Show me how to create an Azure Function"

**Multi-Agent Queries:**
- "I'm starting as a cloud engineer. Who should I connect with and what should I learn?"

## Project Structure

```
lesson-4-agentdeployment/
├── .env.example                 # Environment variables template
├── implementation-plan.md       # Detailed implementation guide
├── README.md                    # This file
├── hosted-agent/               # Azure AI Foundry hosted agent
│   ├── main.py                 # Multi-agent workflow implementation
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container definition
│   └── agent.yaml              # Agent deployment configuration
└── chatkit-server/             # ChatKit server application
    ├── app.py                  # FastAPI backend
    ├── store.py                # SQLite persistence layer
    ├── requirements.txt        # Python dependencies
    └── frontend/               # React frontend
        ├── package.json
        ├── vite.config.ts
        ├── tsconfig.json
        ├── index.html
        └── src/
            ├── main.tsx
            ├── App.tsx
            ├── App.css
            └── index.css
```

## The Multi-Agent Workflow

The hosted agent uses **HandoffBuilder** to orchestrate four specialized agents:

| Agent | Role | Tools |
|-------|------|-------|
| **Triage Agent** | Coordinator - routes queries to specialists | None |
| **Employee Search Agent** | Finds colleagues and team members | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Creates learning paths and recommendations | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generates code samples and guidance | None |

The workflow allows:
- Triage → Any specialist
- Specialists → Other specialists (for related queries)
- Specialists → Triage (for new topics)

## Troubleshooting

### Agent not responding
- Verify the hosted agent is deployed and running in Azure AI Foundry
- Check the `HOSTED_AGENT_NAME` and `HOSTED_AGENT_VERSION` match your deployment

### Vector store errors
- Ensure `VECTOR_STORE_ID` is set correctly
- Verify the vector store contains the employee data

### Authentication errors
- Run `az login` to refresh credentials
- Ensure you have access to the Azure AI Foundry project

## Resources

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)
