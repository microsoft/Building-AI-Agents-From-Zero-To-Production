<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:23:51+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "kn"
}
-->
# ಪಾಠ 4: Azure AI Foundry ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್‌ಗಳೊಂದಿಗೆ ಏಜೆಂಟ್ ನಿಯೋಜನೆ + ChatKit

ಈ ಪಾಠವು ಬಹು ಏಜೆಂಟ್ ವರ್ಕ್‌ಫ್ಲೋವನ್ನು Azure AI Foundry ಗೆ ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್ ಆಗಿ ನಿಯೋಜಿಸುವುದನ್ನು ಮತ್ತು ಅದಕ್ಕೆ ಸಂವಹನ ಮಾಡಲು ChatKit ಆಧಾರಿತ ಫ್ರಂಟ್‌ಎಂಡ್ ಅನ್ನು ರಚಿಸುವುದನ್ನು ತೋರಿಸುತ್ತದೆ.

## ವಾಸ್ತುಶಿಲ್ಪ

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

## ಪೂರ್ವಾಪೇಕ್ಷೆಗಳು

1. ಉತ್ತರ ಮಧ್ಯ ಅಮೆರಿಕಾ ಪ್ರದೇಶದಲ್ಲಿ **Azure AI Foundry ಪ್ರಾಜೆಕ್ಟ್**
2. **Azure CLI** ಪ್ರಾಮಾಣೀಕೃತ (`az login`)
3. **Azure Developer CLI** (`azd`) ಸ್ಥಾಪಿಸಲಾಗಿದೆ
4. **Python 3.12+** ಮತ್ತು **Node.js 18+**
5. ಉದ್ಯೋಗಿ ಡೇಟಾ ಹೊಂದಿರುವ **ವೆಕ್ಟರ್ ಸ್ಟೋರ್** ರಚಿಸಲಾಗಿದೆ

## ತ್ವರಿತ ಪ್ರಾರಂಭ

### 1. ಪರಿಸರ ಚರಗಳನ್ನು ಸೆಟ್ ಮಾಡಿ

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# ನಿಮ್ಮ Azure AI Foundry ಯೋಜನೆಯ ವಿವರಗಳೊಂದಿಗೆ .env ಅನ್ನು ಸಂಪಾದಿಸಿ
```

### 2. ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್ ಅನ್ನು ನಿಯೋಜಿಸಿ

**ಆಯ್ಕೆ A: Azure Developer CLI ಬಳಸಿ (ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**ಆಯ್ಕೆ B: ಡೋಕರ್ + Azure ಕಂಟೈನರ್ ರಿಜಿಸ್ಟ್ರಿ ಬಳಸಿ**

```bash
cd hosted-agent

# ಕಂಟೈನರ್ ನಿರ್ಮಿಸಿ
docker build -t developer-onboarding-agent:latest .

# ACR ಗಾಗಿ ಟ್ಯಾಗ್
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR ಗೆ ಪುಷ್ ಮಾಡಿ
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ಅಜೂರ್ AI ಫೌಂಡ್ರಿ ಪೋರ್ಟಲ್ ಅಥವಾ SDK ಮೂಲಕ ನಿಯೋಜಿಸಿ
```

### 3. ChatKit ಬ್ಯಾಕೆಂಡ್ ಪ್ರಾರಂಭಿಸಿ

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # ವಿಂಡೋಸ್‌ನಲ್ಲಿ: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

ಸರ್ವರ್ `http://localhost:8001` ನಲ್ಲಿ ಪ್ರಾರಂಭವಾಗುತ್ತದೆ

### 4. ChatKit ಫ್ರಂಟ್‌ಎಂಡ್ ಪ್ರಾರಂಭಿಸಿ

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ಫ್ರಂಟ್‌ಎಂಡ್ `http://localhost:3000` ನಲ್ಲಿ ಪ್ರಾರಂಭವಾಗುತ್ತದೆ

### 5. ಅಪ್ಲಿಕೇಶನ್ ಪರೀಕ್ಷಿಸಿ

ನಿಮ್ಮ ಬ್ರೌಸರ್‌ನಲ್ಲಿ `http://localhost:3000` ತೆರೆಯಿರಿ ಮತ್ತು ಈ ಪ್ರಶ್ನೆಗಳನ್ನು ಪ್ರಯತ್ನಿಸಿ:

**ಉದ್ಯೋಗಿ ಹುಡುಕಾಟ:**
- "ನಾನು ಇಲ್ಲಿ ಹೊಸವನಾಗಿದ್ದೇನೆ! ಯಾರಾದರೂ Microsoft ನಲ್ಲಿ ಕೆಲಸ ಮಾಡಿದ್ದಾರಾ?"
- "ಯಾರಿಗೆ Azure Functions ನಲ್ಲಿ ಅನುಭವವಿದೆ?"

**ಕಲಿಕೆ ಸಂಪನ್ಮೂಲಗಳು:**
- "Kubernetes ಗಾಗಿ ಕಲಿಕೆ ಮಾರ್ಗವನ್ನು ರಚಿಸಿ"
- "ಮೇಘ ವಾಸ್ತುಶಿಲ್ಪಕ್ಕಾಗಿ ಯಾವ ಪ್ರಮಾಣಪತ್ರಗಳನ್ನು ಪಡೆಯಬೇಕು?"

**ಕೋಡಿಂಗ್ ಸಹಾಯ:**
- "CosmosDB ಗೆ ಸಂಪರ್ಕಿಸಲು Python ಕೋಡ್ ಬರೆಯಲು ಸಹಾಯ ಮಾಡಿ"
- "ನನಗೆ Azure Function ರಚಿಸುವ ವಿಧಾನ ತೋರಿಸಿ"

**ಬಹು ಏಜೆಂಟ್ ಪ್ರಶ್ನೆಗಳು:**
- "ನಾನು ಕ್ಲೌಡ್ ಎಂಜಿನಿಯರ್ ಆಗಿ ಪ್ರಾರಂಭಿಸುತ್ತಿದ್ದೇನೆ. ಯಾರೊಂದಿಗೆ ಸಂಪರ್ಕಿಸಬೇಕು ಮತ್ತು ಏನು ಕಲಿಯಬೇಕು?"

## ಪ್ರಾಜೆಕ್ಟ್ ರಚನೆ

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

## ಬಹು ಏಜೆಂಟ್ ವರ್ಕ್‌ಫ್ಲೋ

ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್ **HandoffBuilder** ಬಳಸಿ ನಾಲ್ಕು ವಿಶೇಷ ಏಜೆಂಟ್‌ಗಳನ್ನು ಸಂಯೋಜಿಸುತ್ತದೆ:

| ಏಜೆಂಟ್ | ಪಾತ್ರ | ಉಪಕರಣಗಳು |
|---------|-------|------------|
| **ಟ್ರೈಯಾಜ್ ಏಜೆಂಟ್** | ಸಂಯೋಜಕ - ಪ್ರಶ್ನೆಗಳನ್ನು ತಜ್ಞರಿಗೆ ಮಾರ್ಗದರ್ಶನ ಮಾಡುತ್ತದೆ | ಇಲ್ಲ |
| **ಉದ್ಯೋಗಿ ಹುಡುಕಾಟ ಏಜೆಂಟ್** | ಸಹೋದ್ಯೋಗಿಗಳು ಮತ್ತು ತಂಡದ ಸದಸ್ಯರನ್ನು ಹುಡುಕುತ್ತದೆ | HostedFileSearchTool (ವೆಕ್ಟರ್ ಸ್ಟೋರ್) |
| **ಕಲಿಕೆ ಏಜೆಂಟ್** | ಕಲಿಕೆ ಮಾರ್ಗಗಳು ಮತ್ತು ಶಿಫಾರಸುಗಳನ್ನು ರಚಿಸುತ್ತದೆ | HostedMCPTool (Microsoft Learn) |
| **ಕೋಡಿಂಗ್ ಏಜೆಂಟ್** | ಕೋಡ್ ಮಾದರಿಗಳು ಮತ್ತು ಮಾರ್ಗದರ್ಶನವನ್ನು ರಚಿಸುತ್ತದೆ | ಇಲ್ಲ |

ವರ್ಕ್‌ಫ್ಲೋ ಅನುಮತಿಸುತ್ತದೆ:
- ಟ್ರೈಯಾಜ್ → ಯಾವುದೇ ತಜ್ಞ
- ತಜ್ಞರು → ಇತರ ತಜ್ಞರು (ಸಂಬಂಧಿತ ಪ್ರಶ್ನೆಗಳಿಗೆ)
- ತಜ್ಞರು → ಟ್ರೈಯಾಜ್ (ಹೊಸ ವಿಷಯಗಳಿಗೆ)

## ಸಮಸ್ಯೆ ಪರಿಹಾರ

### ಏಜೆಂಟ್ ಪ್ರತಿಕ್ರಿಯಿಸದಿದ್ದರೆ
- ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್ Azure AI Foundry ನಲ್ಲಿ ನಿಯೋಜಿತ ಮತ್ತು ಚಾಲನೆಯಲ್ಲಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ
- `HOSTED_AGENT_NAME` ಮತ್ತು `HOSTED_AGENT_VERSION` ನಿಮ್ಮ ನಿಯೋಜನೆಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ

### ವೆಕ್ಟರ್ ಸ್ಟೋರ್ ದೋಷಗಳು
- `VECTOR_STORE_ID` ಸರಿಯಾಗಿ ಸೆಟ್ ಆಗಿದೆಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ
- ವೆಕ್ಟರ್ ಸ್ಟೋರ್ ಉದ್ಯೋಗಿ ಡೇಟಾವನ್ನು ಹೊಂದಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ

### ಪ್ರಾಮಾಣೀಕರಣ ದೋಷಗಳು
- `az login` ಅನ್ನು ಚಲಾಯಿಸಿ ಪ್ರಮಾಣಪತ್ರಗಳನ್ನು ನವೀಕರಿಸಿ
- ನೀವು Azure AI Foundry ಪ್ರಾಜೆಕ್ಟ್‌ಗೆ ಪ್ರವೇಶ ಹೊಂದಿದ್ದೀರಾ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ

## ಸಂಪನ್ಮೂಲಗಳು

- [Azure AI Foundry ಹೋಸ್ಟ್ ಮಾಡಿದ ಏಜೆಂಟ್‌ಗಳ ಡಾಕ್ಯುಮೆಂಟೇಶನ್](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft ಏಜೆಂಟ್ ಫ್ರೇಮ್ವರ್ಕ್](https://github.com/microsoft/agent-framework)
- [ChatKit ಇಂಟಿಗ್ರೇಶನ್ ಮಾದರಿ](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ಅಸ್ವೀಕರಣ**:  
ಈ ದಸ್ತಾವೇಜು AI ಅನುವಾದ ಸೇವೆ [Co-op Translator](https://github.com/Azure/co-op-translator) ಬಳಸಿ ಅನುವಾದಿಸಲಾಗಿದೆ. ನಾವು ನಿಖರತೆಯಿಗಾಗಿ ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದರೂ, ಸ್ವಯಂಚಾಲಿತ ಅನುವಾದಗಳಲ್ಲಿ ದೋಷಗಳು ಅಥವಾ ಅಸತ್ಯತೆಗಳು ಇರಬಹುದು ಎಂದು ದಯವಿಟ್ಟು ಗಮನಿಸಿ. ಮೂಲ ಭಾಷೆಯಲ್ಲಿರುವ ಮೂಲ ದಸ್ತಾವೇಜನ್ನು ಅಧಿಕೃತ ಮೂಲವಾಗಿ ಪರಿಗಣಿಸಬೇಕು. ಪ್ರಮುಖ ಮಾಹಿತಿಗಾಗಿ, ವೃತ್ತಿಪರ ಮಾನವ ಅನುವಾದವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗುತ್ತದೆ. ಈ ಅನುವಾದ ಬಳಕೆಯಿಂದ ಉಂಟಾಗುವ ಯಾವುದೇ ತಪ್ಪು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವಿಕೆ ಅಥವಾ ತಪ್ಪು ವಿವರಣೆಗಳಿಗೆ ನಾವು ಹೊಣೆಗಾರರಾಗುವುದಿಲ್ಲ.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->