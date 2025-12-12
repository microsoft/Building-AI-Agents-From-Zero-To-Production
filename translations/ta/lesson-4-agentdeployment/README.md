<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:20:28+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ta"
}
-->
# பாடம் 4: Azure AI Foundry ஹோஸ்ட் செய்யப்பட்ட முகவர்களுடன் முகவர் 배치 + ChatKit

இந்த பாடம் ஒரு பன்முகவர் வேலைப்பாட்டை Azure AI Foundry-க்கு ஹோஸ்ட் செய்யப்பட்ட முகவராக 배치 செய்வது மற்றும் அதனுடன் தொடர்பு கொள்ள ChatKit அடிப்படையிலான முன்னணி உருவாக்குவது எப்படி என்பதை காட்டுகிறது.

## கட்டமைப்பு

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

## முன் தேவைகள்

1. வடக்கு மத்திய அமெரிக்கா பிராந்தியத்தில் **Azure AI Foundry திட்டம்**
2. **Azure CLI** அங்கீகாரம் பெற்றது (`az login`)
3. **Azure Developer CLI** (`azd`) நிறுவப்பட்டது
4. **Python 3.12+** மற்றும் **Node.js 18+**
5. ஊழியர் தரவுடன் உருவாக்கப்பட்ட **வெக்டர் ஸ்டோர்**

## விரைவு துவக்கம்

### 1. சுற்றுச்சூழல் மாறிலிகளை அமைக்கவும்

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# உங்கள் Azure AI Foundry திட்ட விவரங்களுடன் .env ஐ திருத்தவும்
```

### 2. ஹோஸ்ட் செய்யப்பட்ட முகவரைக் 배치 செய்யவும்

**விருப்பம் A: Azure Developer CLI பயன்படுத்துதல் (பரிந்துரைக்கப்படுகிறது)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**விருப்பம் B: Docker + Azure Container Registry பயன்படுத்துதல்**

```bash
cd hosted-agent

# கன்டெய்னரை கட்டமைக்கவும்
docker build -t developer-onboarding-agent:latest .

# ACR க்கான டேக்
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR க்கு புஷ் செய்யவும்
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry போர்டல் அல்லது SDK மூலம் வெளியிடவும்
```

### 3. ChatKit பின்புறத்தை துவக்கவும்

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # விண்டோஸில்: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

சேவையகம் `http://localhost:8001` இல் துவங்கும்

### 4. ChatKit முன்னணியை துவக்கவும்

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

முன்னணி `http://localhost:3000` இல் துவங்கும்

### 5. பயன்பாட்டை சோதிக்கவும்

உங்கள் உலாவியில் `http://localhost:3000` ஐ திறந்து இந்த கேள்விகளை முயற்சிக்கவும்:

**ஊழியர் தேடல்:**
- "நான் இங்கே புதியவன்! Microsoft-ல் யாராவது பணியாற்றியவரா?"
- "Azure Functions-ல் அனுபவம் உள்ளவர் யார்?"

**கற்றல் வளங்கள்:**
- "Kubernetes க்கான கற்றல் பாதையை உருவாக்கவும்"
- "மேக கட்டமைப்புக்கான எந்த சான்றிதழ்களை நான் பெற வேண்டும்?"

**கோடிங் உதவி:**
- "CosmosDB-க்கு இணைக்க Python கோடு எழுத உதவி செய்"
- "Azure Function உருவாக்குவது எப்படி எனக் காண்பி"

**பன்முகவர் கேள்விகள்:**
- "நான் மேக பொறியாளராக துவங்குகிறேன். யாருடன் தொடர்பு கொள்ள வேண்டும் மற்றும் என்ன கற்றுக்கொள்ள வேண்டும்?"

## திட்ட அமைப்பு

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

## பன்முகவர் வேலைப்பாடு

ஹோஸ்ட் செய்யப்பட்ட முகவர் **HandoffBuilder** ஐ பயன்படுத்தி நான்கு சிறப்பு முகவர்களை ஒருங்கிணைக்கிறது:

| முகவர் | பங்கு | கருவிகள் |
|-------|------|----------|
| **Triage முகவர்** | ஒருங்கிணைப்பாளர் - கேள்விகளை நிபுணர்களுக்கு வழிமாற்றம் செய்கிறது | எதுவும் இல்லை |
| **ஊழியர் தேடல் முகவர்** | சக ஊழியர்கள் மற்றும் குழு உறுப்பினர்களை கண்டுபிடிக்கிறது | HostedFileSearchTool (வெக்டர் ஸ்டோர்) |
| **கற்றல் முகவர்** | கற்றல் பாதைகள் மற்றும் பரிந்துரைகளை உருவாக்குகிறது | HostedMCPTool (Microsoft Learn) |
| **கோடிங் முகவர்** | கோடு மாதிரிகள் மற்றும் வழிகாட்டுதலை உருவாக்குகிறது | எதுவும் இல்லை |

வேலைப்பாடு அனுமதிக்கிறது:
- Triage → எந்த நிபுணருக்கும்
- நிபுணர்கள் → பிற நிபுணர்களுக்கு (சம்பந்தப்பட்ட கேள்விகளுக்கு)
- நிபுணர்கள் → Triage (புதிய தலைப்புகளுக்கு)

## பிழைதிருத்தம்

### முகவர் பதிலளிக்கவில்லை
- ஹோஸ்ட் செய்யப்பட்ட முகவர் Azure AI Foundry-வில் 배치 செய்யப்பட்டு இயங்குகிறதா என்பதை சரிபார்க்கவும்
- `HOSTED_AGENT_NAME` மற்றும் `HOSTED_AGENT_VERSION` உங்கள் 배치 உடன் பொருந்துகிறதா என்பதை சரிபார்க்கவும்

### வெக்டர் ஸ்டோர் பிழைகள்
- `VECTOR_STORE_ID` சரியாக அமைக்கப்பட்டுள்ளதா என்பதை உறுதிப்படுத்தவும்
- வெக்டர் ஸ்டோர் ஊழியர் தரவை கொண்டுள்ளதா என்பதை சரிபார்க்கவும்

### அங்கீகார பிழைகள்
- அங்கீகாரங்களை புதுப்பிக்க `az login` இயக்கவும்
- Azure AI Foundry திட்டத்திற்கு அணுகல் உங்களிடம் உள்ளதா என்பதை உறுதிப்படுத்தவும்

## வளங்கள்

- [Azure AI Foundry ஹோஸ்ட் செய்யப்பட்ட முகவர்கள் ஆவணங்கள்](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft முகவர் கட்டமைப்பு](https://github.com/microsoft/agent-framework)
- [ChatKit ஒருங்கிணைப்பு மாதிரி](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**குறிப்பு**:  
இந்த ஆவணம் AI மொழிபெயர்ப்பு சேவை [Co-op Translator](https://github.com/Azure/co-op-translator) மூலம் மொழிபெயர்க்கப்பட்டுள்ளது. நாங்கள் துல்லியத்திற்காக முயற்சித்தாலும், தானியங்கி மொழிபெயர்ப்புகளில் பிழைகள் அல்லது தவறுகள் இருக்கக்கூடும் என்பதை தயவுசெய்து கவனிக்கவும். அசல் ஆவணம் அதன் சொந்த மொழியில் அதிகாரப்பூர்வ மூலமாக கருதப்பட வேண்டும். முக்கியமான தகவல்களுக்கு, தொழில்முறை மனித மொழிபெயர்ப்பை பரிந்துரைக்கிறோம். இந்த மொழிபெயர்ப்பின் பயன்பாட்டால் ஏற்படும் எந்த தவறான புரிதல்கள் அல்லது தவறான விளக்கங்களுக்கும் நாங்கள் பொறுப்பேற்கமாட்டோம்.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->