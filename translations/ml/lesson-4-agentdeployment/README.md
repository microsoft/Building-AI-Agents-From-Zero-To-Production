<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:23:09+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ml"
}
-->
# പാഠം 4: Azure AI Foundry ഹോസ്റ്റഡ് ഏജന്റുകളുമായി ഏജന്റ് വിന്യാസം + ChatKit

ഈ പാഠം ഒരു മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോ Azure AI Foundry-യിൽ ഹോസ്റ്റഡ് ഏജന്റായി വിന്യസിച്ച് അതുമായി സംവദിക്കാൻ ChatKit അടിസ്ഥാനമാക്കിയ ഫ്രണ്ട്‌എൻഡ് സൃഷ്ടിക്കുന്ന വിധം കാണിക്കുന്നു.

## ആർക്കിടെക്ചർ

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

## മുൻകൂട്ടി ആവശ്യമായവ

1. **Azure AI Foundry പ്രോജക്ട്** North Central US മേഖലയിൽ
2. **Azure CLI** പ്രാമാണീകരിച്ചിരിക്കുന്നത് (`az login`)
3. **Azure Developer CLI** (`azd`) ഇൻസ്റ്റാൾ ചെയ്തിരിക്കുന്നത്
4. **Python 3.12+** കൂടാതെ **Node.js 18+**
5. **Vector Store** ജീവനക്കാരുടെ ഡാറ്റയോടെ സൃഷ്ടിച്ചിരിക്കുന്നത്

## വേഗത്തിലുള്ള ആരംഭം

### 1. പരിസ്ഥിതി വ്യത്യാസങ്ങൾ സജ്ജമാക്കുക

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# നിങ്ങളുടെ Azure AI Foundry പ്രോജക്ട് വിശദാംശങ്ങളുമായി .env എഡിറ്റ് ചെയ്യുക
```

### 2. ഹോസ്റ്റഡ് ഏജന്റ് വിന്യസിക്കുക

**ഓപ്ഷൻ A: Azure Developer CLI ഉപയോഗിച്ച് (ശുപാർശ ചെയ്യുന്നു)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**ഓപ്ഷൻ B: Docker + Azure Container Registry ഉപയോഗിച്ച്**

```bash
cd hosted-agent

# കണ്ടെയ്‌നർ നിർമ്മിക്കുക
docker build -t developer-onboarding-agent:latest .

# ACR-ക്കുള്ള ടാഗ്
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR-ലേക്ക് പുഷ് ചെയ്യുക
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry പോർട്ടലിലൂടെയോ SDK-യിലൂടെയോ വിന്യസിക്കുക
```

### 3. ChatKit ബാക്ക്‌എൻഡ് ആരംഭിക്കുക

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows-ൽ: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

സർവർ `http://localhost:8001`-ൽ ആരംഭിക്കും

### 4. ChatKit ഫ്രണ്ട്‌എൻഡ് ആരംഭിക്കുക

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ഫ്രണ്ട്‌എൻഡ് `http://localhost:3000`-ൽ ആരംഭിക്കും

### 5. ആപ്ലിക്കേഷൻ പരീക്ഷിക്കുക

നിങ്ങളുടെ ബ്രൗസറിൽ `http://localhost:3000` തുറന്ന് ഈ ചോദ്യങ്ങൾ പരീക്ഷിക്കുക:

**ജീവനക്കാരൻ തിരയൽ:**
- "ഞാൻ ഇവിടെ പുതിയവനാണ്! മൈക്രോസോഫ്റ്റിൽ ആരെങ്കിലും ജോലി ചെയ്തിട്ടുണ്ടോ?"
- "ആസ്യൂർ ഫംഗ്ഷനുകളുമായി പരിചയമുള്ളവർ ആരാണ്?"

**പഠന വിഭവങ്ങൾ:**
- "കുബർണീറ്റിസിനായി ഒരു പഠന പാത സൃഷ്ടിക്കുക"
- "ക്ലൗഡ് ആർക്കിടെക്ചറിനായി എങ്ങനെ സർട്ടിഫിക്കേഷനുകൾ നേടണം?"

**കോഡിംഗ് സഹായം:**
- "CosmosDB-യുമായി ബന്ധിപ്പിക്കുന്ന Python കോഡ് എഴുതാൻ സഹായിക്കൂ"
- "Azure Function സൃഷ്ടിക്കുന്ന വിധം കാണിക്കൂ"

**മൾട്ടി-ഏജന്റ് ചോദ്യങ്ങൾ:**
- "ഞാൻ ക്ലൗഡ് എഞ്ചിനീയറായി ആരംഭിക്കുന്നു. ആരുമായി ബന്ധപ്പെടണം, എന്ത് പഠിക്കണം?"

## പ്രോജക്ട് ഘടന

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

## മൾട്ടി-ഏജന്റ് വർക്ക്‌ഫ്ലോ

ഹോസ്റ്റഡ് ഏജന്റ് **HandoffBuilder** ഉപയോഗിച്ച് നാല് പ്രത്യേക ഏജന്റുകളെ ഏകോപിപ്പിക്കുന്നു:

| ഏജന്റ് | പങ്ക് | ഉപകരണങ്ങൾ |
|-------|------|-------------|
| **ട്രയാജ് ഏജന്റ്** | കോഓർഡിനേറ്റർ - ചോദ്യങ്ങൾ വിദഗ്ധരിലേക്ക് റൂട്ടുചെയ്യുന്നു | ഒന്നുമില്ല |
| **ജീവനക്കാരൻ തിരയൽ ഏജന്റ്** | സഹപ്രവർത്തകരെയും ടീമംഗങ്ങളെയും കണ്ടെത്തുന്നു | HostedFileSearchTool (Vector Store) |
| **പഠന ഏജന്റ്** | പഠന പാതകളും ശുപാർശകളും സൃഷ്ടിക്കുന്നു | HostedMCPTool (Microsoft Learn) |
| **കോഡിംഗ് ഏജന്റ്** | കോഡ് സാമ്പിളുകളും മാർഗ്ഗനിർദേശവും സൃഷ്ടിക്കുന്നു | ഒന്നുമില്ല |

വർക്ക്‌ഫ്ലോ അനുവദിക്കുന്നു:
- ട്രയാജ് → ഏതെങ്കിലും വിദഗ്ധൻ
- വിദഗ്ധർ → മറ്റ് വിദഗ്ധർ (ബന്ധപ്പെട്ട ചോദ്യങ്ങൾക്ക്)
- വിദഗ്ധർ → ട്രയാജ് (പുതിയ വിഷയങ്ങൾക്ക്)

## പ്രശ്നപരിഹാരം

### ഏജന്റ് പ്രതികരിക്കുന്നില്ല
- ഹോസ്റ്റഡ് ഏജന്റ് Azure AI Foundry-യിൽ വിന്യസിച്ചും പ്രവർത്തിച്ചും ഉണ്ടെന്ന് ഉറപ്പാക്കുക
- `HOSTED_AGENT_NAME` ഉം `HOSTED_AGENT_VERSION` ഉം നിങ്ങളുടെ വിന്യാസവുമായി പൊരുത്തപ്പെടുന്നുണ്ടെന്ന് പരിശോധിക്കുക

### വെക്ടർ സ്റ്റോർ പിശകുകൾ
- `VECTOR_STORE_ID` ശരിയായി സജ്ജമാക്കിയിട്ടുണ്ടെന്ന് ഉറപ്പാക്കുക
- വെക്ടർ സ്റ്റോർ ജീവനക്കാരുടെ ഡാറ്റ ഉൾക്കൊള്ളുന്നതായി പരിശോധിക്കുക

### പ്രാമാണീകരണ പിശകുകൾ
- ക്രെഡൻഷ്യലുകൾ പുതുക്കാൻ `az login` ഓടിക്കുക
- Azure AI Foundry പ്രോജക്ടിലേക്ക് നിങ്ങളുടെ ആക്‌സസ് ഉറപ്പാക്കുക

## വിഭവങ്ങൾ

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**അസൂയാ**:  
ഈ രേഖ AI വിവർത്തന സേവനം [Co-op Translator](https://github.com/Azure/co-op-translator) ഉപയോഗിച്ച് വിവർത്തനം ചെയ്തതാണ്. നാം കൃത്യതയ്ക്ക് ശ്രമിച്ചെങ്കിലും, സ്വയം പ്രവർത്തിക്കുന്ന വിവർത്തനങ്ങളിൽ പിശകുകൾ അല്ലെങ്കിൽ തെറ്റുകൾ ഉണ്ടാകാമെന്ന് ദയവായി ശ്രദ്ധിക്കുക. അതിന്റെ മാതൃഭാഷയിലുള്ള യഥാർത്ഥ രേഖയാണ് പ്രാമാണികമായ ഉറവിടം എന്ന് പരിഗണിക്കേണ്ടതാണ്. നിർണായകമായ വിവരങ്ങൾക്ക്, പ്രൊഫഷണൽ മനുഷ്യ വിവർത്തനം ശുപാർശ ചെയ്യപ്പെടുന്നു. ഈ വിവർത്തനം ഉപയോഗിക്കുന്നതിൽ നിന്നുണ്ടാകുന്ന ഏതെങ്കിലും തെറ്റിദ്ധാരണകൾക്കോ തെറ്റായ വ്യാഖ്യാനങ്ങൾക്കോ ഞങ്ങൾ ഉത്തരവാദികളല്ല.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->