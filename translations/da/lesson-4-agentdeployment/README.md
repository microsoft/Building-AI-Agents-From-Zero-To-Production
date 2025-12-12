<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:06:47+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "da"
}
-->
# Lesson 4: Agentudrulning med Azure AI Foundry Hosted Agents + ChatKit

Denne lektion demonstrerer, hvordan man udruller en multi-agent arbejdsgang til Azure AI Foundry som en hosted agent og opretter en ChatKit-baseret frontend til at interagere med den.

## Arkitektur

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

## Forudsætninger

1. **Azure AI Foundry-projekt** i North Central US-regionen
2. **Azure CLI** autentificeret (`az login`)
3. **Azure Developer CLI** (`azd`) installeret
4. **Python 3.12+** og **Node.js 18+**
5. **Vector Store** oprettet med medarbejderdata

## Hurtig start

### 1. Opsæt miljøvariabler

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Rediger .env med dine Azure AI Foundry projektoplysninger
```

### 2. Udrul den hosted agent

**Mulighed A: Brug Azure Developer CLI (anbefalet)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Mulighed B: Brug Docker + Azure Container Registry**

```bash
cd hosted-agent

# Byg containeren
docker build -t developer-onboarding-agent:latest .

# Tag til ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Skub til ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Udrul via Azure AI Foundry-portalen eller SDK'en
```

### 3. Start ChatKit-backenden

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Serveren starter på `http://localhost:8001`

### 4. Start ChatKit-frontenden

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend starter på `http://localhost:3000`

### 5. Test applikationen

Åbn `http://localhost:3000` i din browser og prøv disse forespørgsler:

**Medarbejdersøgning:**
- "Jeg er ny her! Har nogen arbejdet hos Microsoft?"
- "Hvem har erfaring med Azure Functions?"

**Læringsressourcer:**
- "Opret en læringssti for Kubernetes"
- "Hvilke certificeringer bør jeg tage for cloud-arkitektur?"

**Kodningshjælp:**
- "Hjælp mig med at skrive Python-kode til at forbinde til CosmosDB"
- "Vis mig, hvordan man opretter en Azure Function"

**Multi-agent forespørgsler:**
- "Jeg starter som cloud engineer. Hvem skal jeg forbinde mig med, og hvad skal jeg lære?"

## Projektstruktur

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

## Multi-agent arbejdsgangen

Den hosted agent bruger **HandoffBuilder** til at orkestrere fire specialiserede agenter:

| Agent | Rolle | Værktøjer |
|-------|-------|-----------|
| **Triage Agent** | Koordinator - dirigerer forespørgsler til specialister | Ingen |
| **Employee Search Agent** | Finder kolleger og teammedlemmer | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Opretter læringsstier og anbefalinger | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Genererer kodeeksempler og vejledning | Ingen |

Arbejdsgangen tillader:
- Triage → Enhver specialist
- Specialister → Andre specialister (for relaterede forespørgsler)
- Specialister → Triage (for nye emner)

## Fejlfinding

### Agent svarer ikke
- Bekræft, at den hosted agent er udrullet og kører i Azure AI Foundry
- Tjek at `HOSTED_AGENT_NAME` og `HOSTED_AGENT_VERSION` matcher din udrulning

### Fejl i vector store
- Sørg for, at `VECTOR_STORE_ID` er korrekt sat
- Bekræft, at vector store indeholder medarbejderdata

### Autentificeringsfejl
- Kør `az login` for at opdatere legitimationsoplysninger
- Sørg for, at du har adgang til Azure AI Foundry-projektet

## Ressourcer

- [Azure AI Foundry Hosted Agents Dokumentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integrations Eksempel](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, bedes du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det oprindelige dokument på dets modersmål bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->