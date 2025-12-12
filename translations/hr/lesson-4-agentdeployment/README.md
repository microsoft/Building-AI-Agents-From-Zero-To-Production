<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:16:50+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "hr"
}
-->
# Lekcija 4: Implementacija agenta s Azure AI Foundry Hosted Agents + ChatKit

Ova lekcija prikazuje kako implementirati višestruki agentni tijek rada u Azure AI Foundry kao hostiranog agenta i stvoriti frontend temeljen na ChatKit za interakciju s njim.

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

## Preduvjeti

1. **Azure AI Foundry projekt** u regiji North Central US
2. **Azure CLI** autentificiran (`az login`)
3. **Azure Developer CLI** (`azd`) instaliran
4. **Python 3.12+** i **Node.js 18+**
5. **Vector Store** kreiran s podacima o zaposlenicima

## Brzi početak

### 1. Postavite varijable okoline

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Uredite .env s detaljima vašeg Azure AI Foundry projekta
```

### 2. Implementirajte hostiranog agenta

**Opcija A: Korištenje Azure Developer CLI (preporučeno)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opcija B: Korištenje Dockera + Azure Container Registry**

```bash
cd hosted-agent

# Izgradi spremnik
docker build -t developer-onboarding-agent:latest .

# Oznaka za ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Gurni u ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Implementiraj putem Azure AI Foundry portala ili SDK-a
```

### 3. Pokrenite ChatKit backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Na Windowsu: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server će se pokrenuti na `http://localhost:8001`

### 4. Pokrenite ChatKit frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend će se pokrenuti na `http://localhost:3000`

### 5. Testirajte aplikaciju

Otvorite `http://localhost:3000` u pregledniku i isprobajte ove upite:

**Pretraživanje zaposlenika:**
- "Novi sam ovdje! Je li netko radio u Microsoftu?"
- "Tko ima iskustva s Azure Functions?"

**Resursi za učenje:**
- "Kreiraj put učenja za Kubernetes"
- "Koje certifikate trebam za arhitekturu u oblaku?"

**Pomoć u kodiranju:**
- "Pomozi mi napisati Python kod za povezivanje s CosmosDB"
- "Pokaži mi kako napraviti Azure Function"

**Višestruki agentni upiti:**
- "Počinjem kao cloud inženjer. S kim se trebam povezati i što trebam naučiti?"

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

## Višestruki agentni tijek rada

Hostirani agent koristi **HandoffBuilder** za orkestraciju četiri specijalizirana agenta:

| Agent | Uloga | Alati |
|-------|-------|-------|
| **Triage Agent** | Koordinator - usmjerava upite specijalistima | Nema |
| **Employee Search Agent** | Pronalazi kolege i članove tima | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Stvara putove učenja i preporuke | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generira primjere koda i upute | Nema |

Tijek rada omogućuje:
- Triage → bilo kojem specijalistu
- Specijalisti → drugim specijalistima (za povezane upite)
- Specijalisti → Triage (za nove teme)

## Rješavanje problema

### Agent ne odgovara
- Provjerite je li hostirani agent implementiran i radi u Azure AI Foundry
- Provjerite podudaraju li se `HOSTED_AGENT_NAME` i `HOSTED_AGENT_VERSION` s vašom implementacijom

### Pogreške u Vector storeu
- Provjerite je li `VECTOR_STORE_ID` ispravno postavljen
- Provjerite sadrži li vector store podatke o zaposlenicima

### Pogreške autentifikacije
- Pokrenite `az login` za osvježavanje vjerodajnica
- Provjerite imate li pristup Azure AI Foundry projektu

## Resursi

- [Azure AI Foundry Hosted Agents Dokumentacija](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integracijski primjer](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Odricanje od odgovornosti**:
Ovaj dokument je preveden korištenjem AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo postići točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za kritične informacije preporučuje se profesionalni ljudski prijevod. Ne snosimo odgovornost za bilo kakva nesporazuma ili pogrešna tumačenja koja proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->