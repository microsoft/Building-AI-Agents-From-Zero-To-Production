<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:02:32+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "it"
}
-->
# Lezione 4: Distribuzione di agenti con Azure AI Foundry Hosted Agents + ChatKit

Questa lezione dimostra come distribuire un flusso di lavoro multi-agente su Azure AI Foundry come agente ospitato e creare un frontend basato su ChatKit per interagire con esso.

## Architettura

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

## Prerequisiti

1. **Progetto Azure AI Foundry** nella regione North Central US
2. **Azure CLI** autenticato (`az login`)
3. **Azure Developer CLI** (`azd`) installato
4. **Python 3.12+** e **Node.js 18+**
5. **Vector Store** creato con dati dei dipendenti

## Avvio rapido

### 1. Configura le variabili d'ambiente

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Modifica .env con i dettagli del tuo progetto Azure AI Foundry
```

### 2. Distribuisci l'agente ospitato

**Opzione A: Usare Azure Developer CLI (Consigliato)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opzione B: Usare Docker + Azure Container Registry**

```bash
cd hosted-agent

# Costruisci il contenitore
docker build -t developer-onboarding-agent:latest .

# Tag per ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Pusha su ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Distribuisci tramite il portale Azure AI Foundry o SDK
```

### 3. Avvia il backend ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Su Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Il server partirà su `http://localhost:8001`

### 4. Avvia il frontend ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Il frontend partirà su `http://localhost:3000`

### 5. Testa l'applicazione

Apri `http://localhost:3000` nel tuo browser e prova queste query:

**Ricerca dipendenti:**
- "Sono nuovo qui! Qualcuno ha lavorato in Microsoft?"
- "Chi ha esperienza con Azure Functions?"

**Risorse di apprendimento:**
- "Crea un percorso di apprendimento per Kubernetes"
- "Quali certificazioni dovrei ottenere per l'architettura cloud?"

**Aiuto con il codice:**
- "Aiutami a scrivere codice Python per connettermi a CosmosDB"
- "Mostrami come creare una Azure Function"

**Query multi-agente:**
- "Sto iniziando come ingegnere cloud. Con chi dovrei connettermi e cosa dovrei imparare?"

## Struttura del progetto

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

## Il flusso di lavoro multi-agente

L'agente ospitato utilizza **HandoffBuilder** per orchestrare quattro agenti specializzati:

| Agente | Ruolo | Strumenti |
|--------|-------|-----------|
| **Agente di triage** | Coordinatore - indirizza le query agli specialisti | Nessuno |
| **Agente di ricerca dipendenti** | Trova colleghi e membri del team | HostedFileSearchTool (Vector Store) |
| **Agente di apprendimento** | Crea percorsi di apprendimento e raccomandazioni | HostedMCPTool (Microsoft Learn) |
| **Agente di codifica** | Genera esempi di codice e guida | Nessuno |

Il flusso di lavoro consente:
- Triage → Qualsiasi specialista
- Specialisti → Altri specialisti (per query correlate)
- Specialisti → Triage (per nuovi argomenti)

## Risoluzione dei problemi

### Agente non risponde
- Verifica che l'agente ospitato sia distribuito e in esecuzione in Azure AI Foundry
- Controlla che `HOSTED_AGENT_NAME` e `HOSTED_AGENT_VERSION` corrispondano alla tua distribuzione

### Errori del vector store
- Assicurati che `VECTOR_STORE_ID` sia impostato correttamente
- Verifica che il vector store contenga i dati dei dipendenti

### Errori di autenticazione
- Esegui `az login` per aggiornare le credenziali
- Assicurati di avere accesso al progetto Azure AI Foundry

## Risorse

- [Documentazione Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Esempio di integrazione ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per garantire l’accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un traduttore umano. Non ci assumiamo alcuna responsabilità per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->