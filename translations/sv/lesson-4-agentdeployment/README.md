<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:06:09+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "sv"
}
-->
# Lektion 4: Agentdistribution med Azure AI Foundry Hosted Agents + ChatKit

Denna lektion visar hur man distribuerar ett arbetsflöde med flera agenter till Azure AI Foundry som en hostad agent och skapar ett ChatKit-baserat frontend för att interagera med det.

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

## Förutsättningar

1. **Azure AI Foundry-projekt** i regionen North Central US
2. **Azure CLI** autentiserad (`az login`)
3. **Azure Developer CLI** (`azd`) installerad
4. **Python 3.12+** och **Node.js 18+**
5. **Vector Store** skapad med anställdas data

## Kom igång snabbt

### 1. Ställ in miljövariabler

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Redigera .env med dina Azure AI Foundry-projektuppgifter
```

### 2. Distribuera den hostade agenten

**Alternativ A: Använd Azure Developer CLI (Rekommenderas)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Alternativ B: Använd Docker + Azure Container Registry**

```bash
cd hosted-agent

# Bygg containern
docker build -t developer-onboarding-agent:latest .

# Tagg för ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Skicka till ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Distribuera via Azure AI Foundry-portalen eller SDK
```

### 3. Starta ChatKit-backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # På Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Servern startar på `http://localhost:8001`

### 4. Starta ChatKit-frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend startar på `http://localhost:3000`

### 5. Testa applikationen

Öppna `http://localhost:3000` i din webbläsare och prova dessa frågor:

**Sökning efter anställda:**
- "Jag är ny här! Har någon jobbat på Microsoft?"
- "Vem har erfarenhet av Azure Functions?"

**Lärresurser:**
- "Skapa en lärväg för Kubernetes"
- "Vilka certifieringar bör jag satsa på för molnarkitektur?"

**Kodningshjälp:**
- "Hjälp mig skriva Python-kod för att ansluta till CosmosDB"
- "Visa mig hur man skapar en Azure Function"

**Frågor med flera agenter:**
- "Jag börjar som molningenjör. Vem ska jag kontakta och vad bör jag lära mig?"

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

## Arbetsflödet med flera agenter

Den hostade agenten använder **HandoffBuilder** för att orkestrera fyra specialiserade agenter:

| Agent | Roll | Verktyg |
|-------|------|---------|
| **Triage Agent** | Koordinator - dirigerar frågor till specialister | Ingen |
| **Employee Search Agent** | Hittar kollegor och teammedlemmar | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Skapar lärvägar och rekommendationer | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Genererar kodexempel och vägledning | Ingen |

Arbetsflödet tillåter:
- Triage → Vilken specialist som helst
- Specialister → Andra specialister (för relaterade frågor)
- Specialister → Triage (för nya ämnen)

## Felsökning

### Agent svarar inte
- Kontrollera att den hostade agenten är distribuerad och körs i Azure AI Foundry
- Kontrollera att `HOSTED_AGENT_NAME` och `HOSTED_AGENT_VERSION` stämmer överens med din distribution

### Fel i Vector Store
- Säkerställ att `VECTOR_STORE_ID` är korrekt inställd
- Verifiera att vector store innehåller anställdas data

### Autentiseringsfel
- Kör `az login` för att uppdatera autentiseringsuppgifter
- Säkerställ att du har åtkomst till Azure AI Foundry-projektet

## Resurser

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen observera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->