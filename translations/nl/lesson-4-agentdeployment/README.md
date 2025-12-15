<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:08:33+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "nl"
}
-->
# Les 4: Agentimplementatie met Azure AI Foundry Gehoste Agents + ChatKit

Deze les laat zien hoe je een multi-agent workflow implementeert naar Azure AI Foundry als een gehoste agent en een ChatKit-gebaseerde frontend maakt om ermee te communiceren.

## Architectuur

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

## Vereisten

1. **Azure AI Foundry-project** in de regio North Central US
2. **Azure CLI** geverifieerd (`az login`)
3. **Azure Developer CLI** (`azd`) geïnstalleerd
4. **Python 3.12+** en **Node.js 18+**
5. **Vector Store** aangemaakt met werknemersgegevens

## Snelstartgids

### 1. Stel Omgevingsvariabelen in

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Bewerk .env met uw Azure AI Foundry projectgegevens
```

### 2. Implementeer de Gehoste Agent

**Optie A: Gebruik Azure Developer CLI (Aanbevolen)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Optie B: Gebruik Docker + Azure Container Registry**

```bash
cd hosted-agent

# Bouw de container
docker build -t developer-onboarding-agent:latest .

# Tag voor ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Push naar ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Implementeer via Azure AI Foundry-portal of SDK
```

### 3. Start de ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Op Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

De server start op `http://localhost:8001`

### 4. Start de ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

De frontend start op `http://localhost:3000`

### 5. Test de Applicatie

Open `http://localhost:3000` in je browser en probeer deze vragen:

**Werknemer Zoeken:**
- "Ik ben nieuw hier! Heeft iemand bij Microsoft gewerkt?"
- "Wie heeft ervaring met Azure Functions?"

**Leerbronnen:**
- "Maak een leertraject voor Kubernetes"
- "Welke certificeringen moet ik nastreven voor cloudarchitectuur?"

**Hulp bij Coderen:**
- "Help me Python-code schrijven om verbinding te maken met CosmosDB"
- "Laat me zien hoe ik een Azure Function maak"

**Multi-Agent Vragen:**
- "Ik begin als cloud engineer. Met wie moet ik contact opnemen en wat moet ik leren?"

## Projectstructuur

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

## De Multi-Agent Workflow

De gehoste agent gebruikt **HandoffBuilder** om vier gespecialiseerde agents te coördineren:

| Agent | Rol | Tools |
|-------|------|-------|
| **Triage Agent** | Coördinator - leidt vragen naar specialisten | Geen |
| **Employee Search Agent** | Vindt collega’s en teamleden | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Maakt leertrajecten en aanbevelingen | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Genereert codevoorbeelden en begeleiding | Geen |

De workflow staat toe:
- Triage → Elke specialist
- Specialisten → Andere specialisten (voor gerelateerde vragen)
- Specialisten → Triage (voor nieuwe onderwerpen)

## Problemen oplossen

### Agent reageert niet
- Controleer of de gehoste agent is geïmplementeerd en draait in Azure AI Foundry
- Controleer of `HOSTED_AGENT_NAME` en `HOSTED_AGENT_VERSION` overeenkomen met je implementatie

### Vector store fouten
- Zorg dat `VECTOR_STORE_ID` correct is ingesteld
- Controleer of de vector store de werknemersgegevens bevat

### Authenticatiefouten
- Voer `az login` uit om de referenties te vernieuwen
- Zorg dat je toegang hebt tot het Azure AI Foundry-project

## Bronnen

- [Azure AI Foundry Gehoste Agents Documentatie](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integratie Voorbeeld](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsdienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet als de gezaghebbende bron worden beschouwd. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->