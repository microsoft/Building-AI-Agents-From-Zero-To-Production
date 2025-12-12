<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:21:45+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "pcm"
}
-->
# Lesson 4: Agent Deployment wit Azure AI Foundry Hosted Agents + ChatKit

Dis lesson dey show how to deploy multi-agent workflow go Azure AI Foundry as hosted agent and create ChatKit-based frontend to interact wit am.

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

1. **Azure AI Foundry Project** for North Central US region
2. **Azure CLI** wey you don authenticate (`az login`)
3. **Azure Developer CLI** (`azd`) wey you don install
4. **Python 3.12+** and **Node.js 18+**
5. **Vector Store** wey get employee data

## Quick Start

### 1. Set Up Environment Variables

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edit .env wit your Azure AI Foundry project details
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

# Build di container
docker build -t developer-onboarding-agent:latest .

# Tag for ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Push go ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Deploy through Azure AI Foundry portal or SDK
```

### 3. Start the ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server go start for `http://localhost:8001`

### 4. Start the ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

The frontend go start for `http://localhost:3000`

### 5. Test the Application

Open `http://localhost:3000` for your browser and try dis kain queries:

**Employee Search:**
- "I be new here! Anybody don work for Microsoft?"
- "Who get experience wit Azure Functions?"

**Learning Resources:**
- "Make learning path for Kubernetes"
- "Which certifications I suppose pursue for cloud architecture?"

**Coding Help:**
- "Help me write Python code to connect to CosmosDB"
- "Show me how to create Azure Function"

**Multi-Agent Queries:**
- "I dey start as cloud engineer. Who I suppose connect wit and wetin I suppose learn?"

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

The hosted agent dey use **HandoffBuilder** to arrange four specialized agents:

| Agent | Role | Tools |
|-------|------|-------|
| **Triage Agent** | Coordinator - dey route queries go specialists | None |
| **Employee Search Agent** | Dey find colleagues and team members | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Dey create learning paths and recommendations | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Dey generate code samples and guidance | None |

The workflow allow:
- Triage → Any specialist
- Specialists → Other specialists (for related queries)
- Specialists → Triage (for new topics)

## Troubleshooting

### Agent no dey respond
- Check say the hosted agent don deploy and dey run for Azure AI Foundry
- Confirm say `HOSTED_AGENT_NAME` and `HOSTED_AGENT_VERSION` match your deployment

### Vector store errors
- Make sure `VECTOR_STORE_ID` dey set correct
- Confirm say vector store get the employee data

### Authentication errors
- Run `az login` to refresh your credentials
- Make sure you get access to Azure AI Foundry project

## Resources

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document na AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator) wey translate am. Even though we dey try make am correct, abeg sabi say automated translation fit get some mistakes or no too correct. The original document wey e dey for im own language na the correct one. If na serious matter, e better make person wey sabi human translation do am. We no go take responsibility if person no understand well or if dem misinterpret anything wey come from this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->