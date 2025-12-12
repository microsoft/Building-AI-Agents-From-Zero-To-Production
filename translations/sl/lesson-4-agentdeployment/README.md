<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:17:26+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "sl"
}
-->
# Lekcija 4: Namestitev agentov z Azure AI Foundry gostovanimi agenti + ChatKit

Ta lekcija prikazuje, kako namestiti večagentni potek dela v Azure AI Foundry kot gostovanega agenta in ustvariti frontend na osnovi ChatKit za interakcijo z njim.

## Arhitektura

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

## Predpogoji

1. **Projekt Azure AI Foundry** v regiji North Central US
2. **Azure CLI** prijavljen (`az login`)
3. **Azure Developer CLI** (`azd`) nameščen
4. **Python 3.12+** in **Node.js 18+**
5. **Vector Store** ustvarjen z zaposlenimi podatki

## Hiter začetek

### 1. Nastavite okoljske spremenljivke

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Uredite .env z vašimi podatki projekta Azure AI Foundry
```

### 2. Namestite gostovanega agenta

**Možnost A: Uporaba Azure Developer CLI (priporočeno)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Možnost B: Uporaba Docker + Azure Container Registry**

```bash
cd hosted-agent

# Zgradi vsebnik
docker build -t developer-onboarding-agent:latest .

# Oznaka za ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Potisni v ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Namesti preko portala Azure AI Foundry ali SDK
```

### 3. Zaženite ChatKit backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Na Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Strežnik se bo zagnal na `http://localhost:8001`

### 4. Zaženite ChatKit frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend se bo zagnal na `http://localhost:3000`

### 5. Preizkusite aplikacijo

Odprite `http://localhost:3000` v vašem brskalniku in preizkusite te poizvedbe:

**Iskanje zaposlenih:**
- "Sem nov tukaj! Ali je kdo delal pri Microsoftu?"
- "Kdo ima izkušnje z Azure Functions?"

**Učni viri:**
- "Ustvari učni načrt za Kubernetes"
- "Katere certifikate naj pridobim za arhitekturo v oblaku?"

**Pomoč pri programiranju:**
- "Pomagaj mi napisati Python kodo za povezavo s CosmosDB"
- "Pokaži mi, kako ustvariti Azure Function"

**Večagentne poizvedbe:**
- "Začenjam kot inženir za oblak. S kom naj se povežem in kaj naj se naučim?"

## Struktura projekta

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

## Večagentni potek dela

Gostovani agent uporablja **HandoffBuilder** za orkestracijo štirih specializiranih agentov:

| Agent | Vloga | Orodja |
|-------|-------|--------|
| **Triage Agent** | Koordinator - usmerja poizvedbe k specialistom | Nobeno |
| **Employee Search Agent** | Najde sodelavce in člane ekipe | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Ustvarja učne poti in priporočila | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generira primere kode in navodila | Nobeno |

Potek dela omogoča:
- Triage → Kateremukoli specialistu
- Specialist → Drugim specialistom (za povezane poizvedbe)
- Specialist → Triage (za nove teme)

## Odpravljanje težav

### Agent ne odgovarja
- Preverite, da je gostovani agent nameščen in deluje v Azure AI Foundry
- Preverite, da se `HOSTED_AGENT_NAME` in `HOSTED_AGENT_VERSION` ujemata z vašo namestitvijo

### Napake v Vector Store
- Prepričajte se, da je `VECTOR_STORE_ID` pravilno nastavljen
- Preverite, da vector store vsebuje podatke o zaposlenih

### Napake pri preverjanju pristnosti
- Zaženite `az login` za osvežitev poverilnic
- Prepričajte se, da imate dostop do projekta Azure AI Foundry

## Viri

- [Dokumentacija Azure AI Foundry gostovanih agentov](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Primer integracije ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas opozarjamo, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku velja za avtoritativni vir. Za ključne informacije priporočamo strokovni človeški prevod. Za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda, ne odgovarjamo.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->