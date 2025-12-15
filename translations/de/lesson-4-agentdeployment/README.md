<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:50:39+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "de"
}
-->
# Lesson 4: Agent Deployment with Azure AI Foundry Hosted Agents + ChatKit

Diese Lektion zeigt, wie man einen Multi-Agent-Workflow als gehosteten Agent in Azure AI Foundry bereitstellt und ein ChatKit-basiertes Frontend erstellt, um mit ihm zu interagieren.

## Architecture

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

## Prerequisites

1. **Azure AI Foundry Projekt** in der Region North Central US
2. **Azure CLI** authentifiziert (`az login`)
3. **Azure Developer CLI** (`azd`) installiert
4. **Python 3.12+** und **Node.js 18+**
5. **Vector Store** mit Mitarbeiterdaten erstellt

## Quick Start

### 1. Set Up Environment Variables

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Bearbeiten Sie die .env-Datei mit Ihren Azure AI Foundry-Projektdetails
```

### 2. Deploy the Hosted Agent

**Option A: Verwendung der Azure Developer CLI (empfohlen)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Option B: Verwendung von Docker + Azure Container Registry**

```bash
cd hosted-agent

# Erstellen Sie den Container
docker build -t developer-onboarding-agent:latest .

# Tag für ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# In ACR pushen
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Bereitstellen über das Azure AI Foundry-Portal oder SDK
```

### 3. Start the ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Unter Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Der Server startet unter `http://localhost:8001`

### 4. Start the ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Das Frontend startet unter `http://localhost:3000`

### 5. Test the Application

Öffnen Sie `http://localhost:3000` in Ihrem Browser und probieren Sie diese Anfragen aus:

**Mitarbeitersuche:**
- "Ich bin neu hier! Hat jemand bei Microsoft gearbeitet?"
- "Wer hat Erfahrung mit Azure Functions?"

**Lernressourcen:**
- "Erstelle einen Lernpfad für Kubernetes"
- "Welche Zertifizierungen sollte ich für Cloud-Architektur anstreben?"

**Programmierungshilfe:**
- "Hilf mir, Python-Code für die Verbindung zu CosmosDB zu schreiben"
- "Zeig mir, wie man eine Azure Function erstellt"

**Multi-Agent-Anfragen:**
- "Ich starte als Cloud Engineer. Mit wem sollte ich mich vernetzen und was sollte ich lernen?"

## Project Structure

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

## The Multi-Agent Workflow

Der gehostete Agent verwendet **HandoffBuilder**, um vier spezialisierte Agenten zu orchestrieren:

| Agent | Rolle | Tools |
|-------|-------|-------|
| **Triage Agent** | Koordinator - leitet Anfragen an Spezialisten weiter | Keine |
| **Employee Search Agent** | Findet Kollegen und Teammitglieder | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Erstellt Lernpfade und Empfehlungen | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generiert Codebeispiele und Anleitungen | Keine |

Der Workflow erlaubt:
- Triage → Jeder Spezialist
- Spezialisten → Andere Spezialisten (für verwandte Anfragen)
- Spezialisten → Triage (für neue Themen)

## Troubleshooting

### Agent antwortet nicht
- Überprüfen Sie, ob der gehostete Agent in Azure AI Foundry bereitgestellt und ausgeführt wird
- Prüfen Sie, ob `HOSTED_AGENT_NAME` und `HOSTED_AGENT_VERSION` mit Ihrer Bereitstellung übereinstimmen

### Vector Store Fehler
- Stellen Sie sicher, dass `VECTOR_STORE_ID` korrekt gesetzt ist
- Vergewissern Sie sich, dass der Vector Store die Mitarbeiterdaten enthält

### Authentifizierungsfehler
- Führen Sie `az login` aus, um die Anmeldeinformationen zu aktualisieren
- Stellen Sie sicher, dass Sie Zugriff auf das Azure AI Foundry Projekt haben

## Resources

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Für wichtige Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Nutzung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->