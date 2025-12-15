<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:12:05+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "sw"
}
-->
# Somo la 4: Utekelezaji wa Wakala kwa kutumia Wakala Waliohifadhiwa wa Azure AI Foundry + ChatKit

Somo hili linaonyesha jinsi ya kupeleka mtiririko wa kazi wa mawakala wengi kwenye Azure AI Foundry kama wakala aliyehifadhiwa na kuunda frontend inayotegemea ChatKit kuingiliana nayo.

## Mimarisho

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

## Mahitaji ya Awali

1. **Mradi wa Azure AI Foundry** katika eneo la North Central US
2. **Azure CLI** imethibitishwa (`az login`)
3. **Azure Developer CLI** (`azd`) imewekwa
4. **Python 3.12+** na **Node.js 18+**
5. **Hifadhi ya Vector** iliyoundwa na data za wafanyakazi

## Anza Haraka

### 1. Weka Mabadiliko ya Mazingira

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Hariri .env na maelezo ya mradi wako wa Azure AI Foundry
```

### 2. Peleka Wakala Aliyehifadhiwa

**Chaguo A: Kutumia Azure Developer CLI (Inapendekezwa)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Chaguo B: Kutumia Docker + Azure Container Registry**

```bash
cd hosted-agent

# Jenga kontena
docker build -t developer-onboarding-agent:latest .

# Lebo kwa ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Sogeza kwa ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Sambaza kupitia lango la Azure AI Foundry au SDK
```

### 3. Anzisha Backend ya ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Kwenye Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Seva itaanza kwenye `http://localhost:8001`

### 4. Anzisha Frontend ya ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend itaanza kwenye `http://localhost:3000`

### 5. Jaribu Programu

Fungua `http://localhost:3000` kwenye kivinjari chako na jaribu maswali haya:

**Utafutaji wa Mfanyakazi:**
- "Mimi ni mpya hapa! Je, kuna mtu aliyewahi kufanya kazi Microsoft?"
- "Nani ana uzoefu na Azure Functions?"

**Rasilimali za Kujifunza:**
- "Tengeneza njia ya kujifunza kwa Kubernetes"
- "Ni vyeti gani ninavyopaswa kufuata kwa usanifu wa wingu?"

**Msaada wa Kuuandika Msimbo:**
- "Nisaidie kuandika msimbo wa Python wa kuungana na CosmosDB"
- "Nionyeshe jinsi ya kuunda Azure Function"

**Maswali ya Wakala Wengi:**
- "Naanza kama mhandisi wa wingu. Nifanye mawasiliano na nani na nifundishwe nini?"

## Muundo wa Mradi

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

## Mtiririko wa Kazi wa Wakala Wengi

Wakala aliyehifadhiwa anatumia **HandoffBuilder** kuratibu mawakala wanne maalum:

| Wakala | Nafasi | Zana |
|--------|--------|------|
| **Wakala wa Triage** | Mratibu - hupeleka maswali kwa wataalamu | Hakuna |
| **Wakala wa Utafutaji wa Mfanyakazi** | Hupata wenzake na wanatimu | HostedFileSearchTool (Hifadhi ya Vector) |
| **Wakala wa Kujifunza** | Huunda njia za kujifunza na mapendekezo | HostedMCPTool (Microsoft Learn) |
| **Wakala wa Kuuandika Msimbo** | Hutengeneza sampuli za msimbo na mwongozo | Hakuna |

Mtiririko wa kazi unaruhusu:
- Triage → Mtaalamu yeyote
- Wataalamu → Wataalamu wengine (kwa maswali yanayohusiana)
- Wataalamu → Triage (kwa mada mpya)

## Utatuzi wa Matatizo

### Wakala haajibu
- Hakikisha wakala aliyehifadhiwa amepelekwa na anaendesha katika Azure AI Foundry
- Angalia `HOSTED_AGENT_NAME` na `HOSTED_AGENT_VERSION` zinaendana na utekelezaji wako

### Makosa ya hifadhi ya vector
- Hakikisha `VECTOR_STORE_ID` imewekwa kwa usahihi
- Thibitisha hifadhi ya vector ina data za wafanyakazi

### Makosa ya uthibitishaji
- Endesha `az login` ili kusasisha vyeti
- Hakikisha una ufikiaji wa mradi wa Azure AI Foundry

## Rasilimali

- [Nyaraka za Wakala Waliohifadhiwa wa Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Mfumo wa Wakala wa Microsoft](https://github.com/microsoft/agent-framework)
- [Mfano wa Uunganisho wa ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kiarifu cha Msamaha**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kwamba tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake ya asili inapaswa kuchukuliwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatubebwi dhamana kwa kutoelewana au tafsiri potofu zinazotokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->