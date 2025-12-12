<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:14:54+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ro"
}
-->
# Lecția 4: Implementarea Agentului cu Azure AI Foundry Hosted Agents + ChatKit

Această lecție demonstrează cum să implementați un flux de lucru multi-agent în Azure AI Foundry ca agent găzduit și să creați un frontend bazat pe ChatKit pentru a interacționa cu acesta.

## Arhitectură

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

## Cerințe preliminare

1. **Proiect Azure AI Foundry** în regiunea North Central US
2. **Azure CLI** autentificat (`az login`)
3. **Azure Developer CLI** (`azd`) instalat
4. **Python 3.12+** și **Node.js 18+**
5. **Vector Store** creat cu datele angajaților

## Pornire rapidă

### 1. Configurați variabilele de mediu

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Editează .env cu detaliile proiectului tău Azure AI Foundry
```

### 2. Implementați agentul găzduit

**Opțiunea A: Folosind Azure Developer CLI (Recomandat)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opțiunea B: Folosind Docker + Azure Container Registry**

```bash
cd hosted-agent

# Construiește containerul
docker build -t developer-onboarding-agent:latest .

# Etichetă pentru ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Împinge către ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Desfășoară prin portalul Azure AI Foundry sau SDK-ul
```

### 3. Porniți backend-ul ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Pe Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Serverul va porni la `http://localhost:8001`

### 4. Porniți frontend-ul ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend-ul va porni la `http://localhost:3000`

### 5. Testați aplicația

Deschideți `http://localhost:3000` în browser și încercați aceste interogări:

**Căutare angajați:**
- "Sunt nou aici! A lucrat cineva la Microsoft?"
- "Cine are experiență cu Azure Functions?"

**Resurse de învățare:**
- "Creează un traseu de învățare pentru Kubernetes"
- "Ce certificări ar trebui să urmez pentru arhitectura cloud?"

**Ajutor la programare:**
- "Ajută-mă să scriu cod Python pentru conectarea la CosmosDB"
- "Arată-mi cum să creez o Azure Function"

**Interogări multi-agent:**
- "Încep ca inginer cloud. Cu cine ar trebui să mă conectez și ce ar trebui să învăț?"

## Structura proiectului

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

## Fluxul de lucru multi-agent

Agentul găzduit folosește **HandoffBuilder** pentru a orchestra patru agenți specializați:

| Agent | Rol | Unelte |
|-------|------|-------|
| **Agent Triage** | Coordinator - direcționează interogările către specialiști | Niciuna |
| **Agent Căutare Angajați** | Găsește colegi și membri ai echipei | HostedFileSearchTool (Vector Store) |
| **Agent Învățare** | Creează trasee de învățare și recomandări | HostedMCPTool (Microsoft Learn) |
| **Agent Programare** | Generează exemple de cod și ghidaj | Niciuna |

Fluxul de lucru permite:
- Triage → Orice specialist
- Specialiști → Alți specialiști (pentru interogări conexe)
- Specialiști → Triage (pentru subiecte noi)

## Depanare

### Agentul nu răspunde
- Verificați dacă agentul găzduit este implementat și rulează în Azure AI Foundry
- Verificați dacă `HOSTED_AGENT_NAME` și `HOSTED_AGENT_VERSION` corespund implementării dvs.

### Erori Vector Store
- Asigurați-vă că `VECTOR_STORE_ID` este setat corect
- Verificați dacă vector store conține datele angajaților

### Erori de autentificare
- Rulați `az login` pentru a reîmprospăta acreditările
- Asigurați-vă că aveți acces la proiectul Azure AI Foundry

## Resurse

- [Documentația Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Exemplu de integrare ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare de responsabilitate**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm răspunderea pentru eventualele neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->