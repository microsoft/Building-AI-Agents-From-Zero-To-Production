<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:07:20+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "no"
}
-->
# Lesson 4: Agentdistribusjon med Azure AI Foundry Hosted Agents + ChatKit

Denne leksjonen viser hvordan du distribuerer en arbeidsflyt med flere agenter til Azure AI Foundry som en hosted agent og lager en ChatKit-basert frontend for å samhandle med den.

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

## Forutsetninger

1. **Azure AI Foundry-prosjekt** i North Central US-regionen
2. **Azure CLI** autentisert (`az login`)
3. **Azure Developer CLI** (`azd`) installert
4. **Python 3.12+** og **Node.js 18+**
5. **Vector Store** opprettet med ansattdata

## Rask start

### 1. Sett opp miljøvariabler

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Rediger .env med detaljene for ditt Azure AI Foundry-prosjekt
```

### 2. Distribuer Hosted Agent

**Alternativ A: Bruke Azure Developer CLI (anbefalt)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Alternativ B: Bruke Docker + Azure Container Registry**

```bash
cd hosted-agent

# Bygg containeren
docker build -t developer-onboarding-agent:latest .

# Tag for ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Push til ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Distribuer via Azure AI Foundry-portalen eller SDK-en
```

### 3. Start ChatKit-backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Serveren starter på `http://localhost:8001`

### 4. Start ChatKit-frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend starter på `http://localhost:3000`

### 5. Test applikasjonen

Åpne `http://localhost:3000` i nettleseren din og prøv disse spørsmålene:

**Ansattsøk:**
- "Jeg er ny her! Har noen jobbet hos Microsoft?"
- "Hvem har erfaring med Azure Functions?"

**Læringsressurser:**
- "Lag en læringssti for Kubernetes"
- "Hvilke sertifiseringer bør jeg ta for skyarkitektur?"

**Kodehjelp:**
- "Hjelp meg å skrive Python-kode for å koble til CosmosDB"
- "Vis meg hvordan jeg lager en Azure Function"

**Spørsmål til flere agenter:**
- "Jeg starter som skyingeniør. Hvem bør jeg kontakte og hva bør jeg lære?"

## Prosjektstruktur

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

## Arbeidsflyten med flere agenter

Den hosted agenten bruker **HandoffBuilder** for å orkestrere fire spesialiserte agenter:

| Agent | Rolle | Verktøy |
|-------|-------|---------|
| **Triage Agent** | Koordinator - ruter forespørsler til spesialister | Ingen |
| **Employee Search Agent** | Finner kolleger og teammedlemmer | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Lager læringsstier og anbefalinger | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Genererer kodeeksempler og veiledning | Ingen |

Arbeidsflyten tillater:
- Triage → Hvilken som helst spesialist
- Spesialister → Andre spesialister (for relaterte spørsmål)
- Spesialister → Triage (for nye temaer)

## Feilsøking

### Agent svarer ikke
- Bekreft at hosted agent er distribuert og kjører i Azure AI Foundry
- Sjekk at `HOSTED_AGENT_NAME` og `HOSTED_AGENT_VERSION` stemmer med distribusjonen din

### Feil med Vector Store
- Sørg for at `VECTOR_STORE_ID` er satt riktig
- Bekreft at vector store inneholder ansattdataene

### Autentiseringsfeil
- Kjør `az login` for å oppdatere legitimasjon
- Sørg for at du har tilgang til Azure AI Foundry-prosjektet

## Ressurser

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->