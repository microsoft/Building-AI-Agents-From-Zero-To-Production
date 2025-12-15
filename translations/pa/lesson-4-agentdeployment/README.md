<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:00:36+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "pa"
}
-->
# Lesson 4: Agent Deployment with Azure AI Foundry Hosted Agents + ChatKit

ਇਸ ਪਾਠ ਵਿੱਚ ਦਿਖਾਇਆ ਗਿਆ ਹੈ ਕਿ ਕਿਵੇਂ ਇੱਕ ਬਹੁ-ਏਜੰਟ ਵਰਕਫਲੋ ਨੂੰ Azure AI Foundry ਵਿੱਚ ਇੱਕ ਹੋਸਟ ਕੀਤੇ ਏਜੰਟ ਵਜੋਂ ਤਾਇਨਾਤ ਕੀਤਾ ਜਾਵੇ ਅਤੇ ਇਸ ਨਾਲ ਇੰਟਰੈਕਟ ਕਰਨ ਲਈ ChatKit-ਅਧਾਰਿਤ ਫਰੰਟਐਂਡ ਬਣਾਇਆ ਜਾਵੇ।

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

1. **Azure AI Foundry Project** ਉੱਤਰ ਮੱਧ US ਖੇਤਰ ਵਿੱਚ
2. **Azure CLI** ਪ੍ਰਮਾਣਿਤ (`az login`)
3. **Azure Developer CLI** (`azd`) ਇੰਸਟਾਲ ਕੀਤਾ ਹੋਇਆ
4. **Python 3.12+** ਅਤੇ **Node.js 18+**
5. **Vector Store** ਕਰਮਚਾਰੀ ਡੇਟਾ ਨਾਲ ਬਣਾਇਆ ਗਿਆ

## Quick Start

### 1. Set Up Environment Variables

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# ਆਪਣੇ Azure AI Foundry ਪ੍ਰੋਜੈਕਟ ਵੇਰਵਿਆਂ ਨਾਲ .env ਨੂੰ ਸੰਪਾਦਿਤ ਕਰੋ
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

# ਕੰਟੇਨਰ ਬਣਾਓ
docker build -t developer-onboarding-agent:latest .

# ACR ਲਈ ਟੈਗ
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR 'ਤੇ ਧੱਕੋ
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry ਪੋਰਟਲ ਜਾਂ SDK ਰਾਹੀਂ ਤਾਇਨਾਤ ਕਰੋ
```

### 3. Start the ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows 'ਤੇ: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

ਸਰਵਰ `http://localhost:8001` 'ਤੇ ਸ਼ੁਰੂ ਹੋਵੇਗਾ

### 4. Start the ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ਫਰੰਟਐਂਡ `http://localhost:3000` 'ਤੇ ਸ਼ੁਰੂ ਹੋਵੇਗਾ

### 5. Test the Application

ਆਪਣੇ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ `http://localhost:3000` ਖੋਲ੍ਹੋ ਅਤੇ ਇਹਨਾਂ ਪ੍ਰਸ਼ਨਾਂ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰੋ:

**ਕਰਮਚਾਰੀ ਖੋਜ:**
- "ਮੈਂ ਇੱਥੇ ਨਵਾਂ ਹਾਂ! ਕੀ ਕਿਸੇ ਨੇ Microsoft ਵਿੱਚ ਕੰਮ ਕੀਤਾ ਹੈ?"
- "ਕਿਸ ਕੋਲ Azure Functions ਦਾ ਅਨੁਭਵ ਹੈ?"

**ਸਿੱਖਣ ਦੇ ਸਰੋਤ:**
- "Kubernetes ਲਈ ਸਿੱਖਣ ਦਾ ਰਸਤਾ ਬਣਾਓ"
- "ਕਲਾਉਡ ਆਰਕੀਟੈਕਚਰ ਲਈ ਮੈਂ ਕਿਹੜੀਆਂ ਸਰਟੀਫਿਕੇਸ਼ਨਾਂ ਕਰਾਂ?"

**ਕੋਡਿੰਗ ਸਹਾਇਤਾ:**
- "CosmosDB ਨਾਲ ਜੁੜਨ ਲਈ Python ਕੋਡ ਲਿਖਣ ਵਿੱਚ ਮਦਦ ਕਰੋ"
- "ਮੈਨੂੰ ਦਿਖਾਓ ਕਿ ਕਿਵੇਂ ਇੱਕ Azure Function ਬਣਾਈਏ"

**ਬਹੁ-ਏਜੰਟ ਪ੍ਰਸ਼ਨ:**
- "ਮੈਂ ਕਲਾਉਡ ਇੰਜੀਨੀਅਰ ਵਜੋਂ ਸ਼ੁਰੂ ਕਰ ਰਿਹਾ ਹਾਂ। ਮੈਨੂੰ ਕਿਸ ਨਾਲ ਜੁੜਨਾ ਚਾਹੀਦਾ ਹੈ ਅਤੇ ਕੀ ਸਿੱਖਣਾ ਚਾਹੀਦਾ ਹੈ?"

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

ਹੋਸਟ ਕੀਤੇ ਏਜੰਟ **HandoffBuilder** ਦੀ ਵਰਤੋਂ ਕਰਦੇ ਹਨ ਜੋ ਚਾਰ ਵਿਸ਼ੇਸ਼ ਏਜੰਟਾਂ ਨੂੰ ਸਮਨਵਿਤ ਕਰਦਾ ਹੈ:

| ਏਜੰਟ | ਭੂਮਿਕਾ | ਸੰਦ |
|-------|---------|-------|
| **Triage Agent** | ਕੋਆਰਡੀਨੇਟਰ - ਪ੍ਰਸ਼ਨਾਂ ਨੂੰ ਵਿਸ਼ੇਸ਼ਜ્ઞਾਂ ਵੱਲ ਭੇਜਦਾ ਹੈ | ਕੋਈ ਨਹੀਂ |
| **Employee Search Agent** | ਸਹਿਕਰਮੀ ਅਤੇ ਟੀਮ ਮੈਂਬਰ ਲੱਭਦਾ ਹੈ | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | ਸਿੱਖਣ ਦੇ ਰਸਤੇ ਅਤੇ ਸਿਫਾਰਸ਼ਾਂ ਬਣਾਉਂਦਾ ਹੈ | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | ਕੋਡ ਨਮੂਨੇ ਅਤੇ ਮਦਦ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ | ਕੋਈ ਨਹੀਂ |

ਵਰਕਫਲੋ ਇਜਾਜ਼ਤ ਦਿੰਦਾ ਹੈ:
- Triage → ਕਿਸੇ ਵੀ ਵਿਸ਼ੇਸ਼ਜ્ઞ ਨੂੰ
- ਵਿਸ਼ੇਸ਼ਜ्ञ → ਹੋਰ ਵਿਸ਼ੇਸ਼ਜ्ञਾਂ ਨੂੰ (ਸੰਬੰਧਿਤ ਪ੍ਰਸ਼ਨਾਂ ਲਈ)
- ਵਿਸ਼ੇਸ਼ਜ्ञ → Triage ਨੂੰ (ਨਵੇਂ ਵਿਸ਼ਿਆਂ ਲਈ)

## Troubleshooting

### ਏਜੰਟ ਜਵਾਬ ਨਹੀਂ ਦੇ ਰਿਹਾ
- ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਹੋਸਟ ਕੀਤਾ ਏਜੰਟ Azure AI Foundry ਵਿੱਚ ਤਾਇਨਾਤ ਅਤੇ ਚੱਲ ਰਿਹਾ ਹੈ
- `HOSTED_AGENT_NAME` ਅਤੇ `HOSTED_AGENT_VERSION` ਤੁਹਾਡੇ ਤਾਇਨਾਤ ਨਾਲ ਮੇਲ ਖਾਂਦੇ ਹਨ ਜਾਂ ਨਹੀਂ ਜਾਂਚੋ

### Vector store ਦੀਆਂ ਗਲਤੀਆਂ
- ਯਕੀਨੀ ਬਣਾਓ ਕਿ `VECTOR_STORE_ID` ਸਹੀ ਤਰੀਕੇ ਨਾਲ ਸੈੱਟ ਹੈ
- ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਵੈਕਟਰ ਸਟੋਰ ਵਿੱਚ ਕਰਮਚਾਰੀ ਡੇਟਾ ਹੈ

### ਪ੍ਰਮਾਣਿਕਤਾ ਦੀਆਂ ਗਲਤੀਆਂ
- `az login` ਚਲਾਓ ਤਾਂ ਜੋ ਪ੍ਰਮਾਣ ਪੱਤਰ ਤਾਜ਼ਾ ਹੋ ਜਾਣ
- ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਤੁਹਾਡੇ ਕੋਲ Azure AI Foundry ਪ੍ਰੋਜੈਕਟ ਦੀ ਪਹੁੰਚ ਹੈ

## Resources

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ਅਸਵੀਕਾਰੋਪੱਤਰ**:  
ਇਹ ਦਸਤਾਵੇਜ਼ AI ਅਨੁਵਾਦ ਸੇਵਾ [Co-op Translator](https://github.com/Azure/co-op-translator) ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਕੀਤਾ ਗਿਆ ਹੈ। ਜਦੋਂ ਕਿ ਅਸੀਂ ਸਹੀਤਾ ਲਈ ਕੋਸ਼ਿਸ਼ ਕਰਦੇ ਹਾਂ, ਕਿਰਪਾ ਕਰਕੇ ਧਿਆਨ ਵਿੱਚ ਰੱਖੋ ਕਿ ਸਵੈਚਾਲਿਤ ਅਨੁਵਾਦਾਂ ਵਿੱਚ ਗਲਤੀਆਂ ਜਾਂ ਅਸਮਰਥਤਾਵਾਂ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਮੂਲ ਦਸਤਾਵੇਜ਼ ਆਪਣੀ ਮੂਲ ਭਾਸ਼ਾ ਵਿੱਚ ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ ਮੰਨਿਆ ਜਾਣਾ ਚਾਹੀਦਾ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ ਲਈ, ਪੇਸ਼ੇਵਰ ਮਨੁੱਖੀ ਅਨੁਵਾਦ ਦੀ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਅਸੀਂ ਇਸ ਅਨੁਵਾਦ ਦੀ ਵਰਤੋਂ ਤੋਂ ਉਤਪੰਨ ਕਿਸੇ ਵੀ ਗਲਤਫਹਿਮੀ ਜਾਂ ਗਲਤ ਵਿਆਖਿਆ ਲਈ ਜ਼ਿੰਮੇਵਾਰ ਨਹੀਂ ਹਾਂ।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->