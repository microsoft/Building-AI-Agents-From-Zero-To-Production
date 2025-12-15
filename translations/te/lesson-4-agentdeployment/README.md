<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:22:24+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "te"
}
-->
# పాఠం 4: Azure AI Foundry హోస్టెడ్ ఏజెంట్స్ + ChatKit తో ఏజెంట్ డిప్లాయ్‌మెంట్

ఈ పాఠం ఒక బహుళ ఏజెంట్ వర్క్‌ఫ్లోను Azure AI Foundryలో హోస్టెడ్ ఏజెంట్‌గా ఎలా డిప్లాయ్ చేయాలో మరియు దానితో ఇంటరాక్ట్ అయ్యేందుకు ChatKit ఆధారిత ఫ్రంట్‌ఎండ్‌ను ఎలా సృష్టించాలో చూపిస్తుంది.

## ఆర్కిటెక్చర్

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

## ముందస్తు అవసరాలు

1. **Azure AI Foundry ప్రాజెక్ట్** నార్త్ సెంట్రల్ US ప్రాంతంలో
2. **Azure CLI** ధృవీకరించబడింది (`az login`)
3. **Azure Developer CLI** (`azd`) ఇన్‌స్టాల్ చేయబడింది
4. **Python 3.12+** మరియు **Node.js 18+**
5. **వెక్టర్ స్టోర్** ఉద్యోగి డేటాతో సృష్టించబడింది

## త్వరిత ప్రారంభం

### 1. పర్యావరణ వేరియబుల్స్ సెట్ చేయండి

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# మీ Azure AI Foundry ప్రాజెక్ట్ వివరాలతో .env ను సవరించండి
```

### 2. హోస్టెడ్ ఏజెంట్‌ను డిప్లాయ్ చేయండి

**ఎంపిక A: Azure Developer CLI ఉపయోగించడం (సిఫార్సు చేయబడింది)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**ఎంపిక B: Docker + Azure కంటైనర్ రిజిస్ట్రీ ఉపయోగించడం**

```bash
cd hosted-agent

# కంటైనర్‌ను నిర్మించండి
docker build -t developer-onboarding-agent:latest .

# ACR కోసం ట్యాగ్
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR కు పుష్ చేయండి
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry పోర్టల్ లేదా SDK ద్వారా డిప్లాయ్ చేయండి
```

### 3. ChatKit బ్యాక్‌ఎండ్ ప్రారంభించండి

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # విండోస్‌లో: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

సర్వర్ `http://localhost:8001` వద్ద ప్రారంభమవుతుంది

### 4. ChatKit ఫ్రంట్‌ఎండ్ ప్రారంభించండి

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ఫ్రంట్‌ఎండ్ `http://localhost:3000` వద్ద ప్రారంభమవుతుంది

### 5. అప్లికేషన్‌ను పరీక్షించండి

మీ బ్రౌజర్‌లో `http://localhost:3000` తెరవండి మరియు ఈ ప్రశ్నలను ప్రయత్నించండి:

**ఉద్యోగి శోధన:**
- "నేను ఇక్కడ కొత్తవాడిని! Microsoftలో ఎవరు పని చేశారు?"
- "Azure Functions అనుభవం ఎవరికుంది?"

**అభ్యాస వనరులు:**
- "Kubernetes కోసం ఒక అభ్యాస మార్గాన్ని సృష్టించండి"
- "క్లౌడ్ ఆర్కిటెక్చర్ కోసం నేను ఏ సర్టిఫికేషన్లు చేయాలి?"

**కోడింగ్ సహాయం:**
- "CosmosDBకి కనెక్ట్ అయ్యేందుకు Python కోడ్ రాయడంలో సహాయం చేయండి"
- "Azure Function ఎలా సృష్టించాలో చూపించండి"

**బహుళ ఏజెంట్ ప్రశ్నలు:**
- "నేను క్లౌడ్ ఇంజనీర్‌గా ప్రారంభిస్తున్నాను. ఎవరి తో కనెక్ట్ కావాలి మరియు ఏమి నేర్చుకోవాలి?"

## ప్రాజెక్ట్ నిర్మాణం

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

## బహుళ ఏజెంట్ వర్క్‌ఫ్లో

హోస్టెడ్ ఏజెంట్ **HandoffBuilder** ఉపయోగించి నాలుగు ప్రత్యేక ఏజెంట్లను సమన్వయిస్తుంది:

| ఏజెంట్ | పాత్ర | టూల్స్ |
|-------|------|-------|
| **ట్రయాజ్ ఏజెంట్** | కోఆర్డినేటర్ - ప్రశ్నలను నిపుణులకు మార్గనిర్దేశం చేస్తుంది | ఏమీ లేదు |
| **ఉద్యోగి శోధన ఏజెంట్** | సహోద్యోగులు మరియు టీమ్ సభ్యులను కనుగొంటుంది | HostedFileSearchTool (వెక్టర్ స్టోర్) |
| **అభ్యాస ఏజెంట్** | అభ్యాస మార్గాలు మరియు సిఫార్సులు సృష్టిస్తుంది | HostedMCPTool (Microsoft Learn) |
| **కోడింగ్ ఏజెంట్** | కోడ్ నమూనాలు మరియు మార్గదర్శకత్వం అందిస్తుంది | ఏమీ లేదు |

వర్క్‌ఫ్లో అనుమతిస్తుంది:
- ట్రయాజ్ → ఏ నిపుణుడు అయినా
- నిపుణులు → ఇతర నిపుణులు (సంబంధిత ప్రశ్నల కోసం)
- నిపుణులు → ట్రయాజ్ (కొత్త విషయాల కోసం)

## సమస్య పరిష్కారం

### ఏజెంట్ స్పందించడంలేదు
- హోస్టెడ్ ఏజెంట్ Azure AI Foundryలో డిప్లాయ్ అయి నడుస్తున్నదని నిర్ధారించుకోండి
- `HOSTED_AGENT_NAME` మరియు `HOSTED_AGENT_VERSION` మీ డిప్లాయ్‌మెంట్‌కు సరిపోతున్నాయా చూడండి

### వెక్టర్ స్టోర్ లో లోపాలు
- `VECTOR_STORE_ID` సరిగ్గా సెట్ చేయబడిందని నిర్ధారించుకోండి
- వెక్టర్ స్టోర్‌లో ఉద్యోగి డేటా ఉందని ధృవీకరించండి

### ధృవీకరణ లోపాలు
- క్రెడెన్షియల్స్ రిఫ్రెష్ చేయడానికి `az login` నడపండి
- Azure AI Foundry ప్రాజెక్ట్‌కు మీకు యాక్సెస్ ఉందని నిర్ధారించుకోండి

## వనరులు

- [Azure AI Foundry Hosted Agents డాక్యుమెంటేషన్](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit ఇంటిగ్రేషన్ సాంపిల్](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**అస్పష్టత**:  
ఈ పత్రాన్ని AI అనువాద సేవ [Co-op Translator](https://github.com/Azure/co-op-translator) ఉపయోగించి అనువదించబడింది. మేము ఖచ్చితత్వానికి ప్రయత్నించినప్పటికీ, ఆటోమేటెడ్ అనువాదాల్లో పొరపాట్లు లేదా తప్పిదాలు ఉండవచ్చు. మూల పత్రం దాని స్వదేశీ భాషలో అధికారిక మూలంగా పరిగణించాలి. ముఖ్యమైన సమాచారానికి, ప్రొఫెషనల్ మానవ అనువాదం సిఫార్సు చేయబడుతుంది. ఈ అనువాదం వాడకంలో ఏర్పడిన ఏవైనా అపార్థాలు లేదా తప్పుదారులు కోసం మేము బాధ్యత వహించము.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->