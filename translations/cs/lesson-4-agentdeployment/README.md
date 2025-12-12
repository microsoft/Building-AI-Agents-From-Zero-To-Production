<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:13:36+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "cs"
}
-->
# Lekce 4: Nasazení agenta s Azure AI Foundry Hosted Agents + ChatKit

Tato lekce ukazuje, jak nasadit workflow s více agenty do Azure AI Foundry jako hostovaného agenta a vytvořit frontend založený na ChatKit pro interakci s ním.

## Architektura

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

## Požadavky

1. **Projekt Azure AI Foundry** v regionu North Central US
2. **Azure CLI** přihlášený (`az login`)
3. **Azure Developer CLI** (`azd`) nainstalovaný
4. **Python 3.12+** a **Node.js 18+**
5. **Vector Store** vytvořený s daty zaměstnanců

## Rychlý start

### 1. Nastavení proměnných prostředí

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Upravte .env s detaily vašeho projektu Azure AI Foundry
```

### 2. Nasazení hostovaného agenta

**Možnost A: Použití Azure Developer CLI (doporučeno)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Možnost B: Použití Docker + Azure Container Registry**

```bash
cd hosted-agent

# Sestavte kontejner
docker build -t developer-onboarding-agent:latest .

# Tag pro ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Push do ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Nasadit přes portál Azure AI Foundry nebo SDK
```

### 3. Spuštění backendu ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Ve Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server se spustí na `http://localhost:8001`

### 4. Spuštění frontendu ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend se spustí na `http://localhost:3000`

### 5. Otestujte aplikaci

Otevřete `http://localhost:3000` ve svém prohlížeči a vyzkoušejte tyto dotazy:

**Vyhledávání zaměstnanců:**
- "Jsem tu nový! Pracoval někdo v Microsoftu?"
- "Kdo má zkušenosti s Azure Functions?"

**Vzdělávací zdroje:**
- "Vytvoř mi vzdělávací cestu pro Kubernetes"
- "Jaké certifikace bych měl získat pro cloudovou architekturu?"

**Pomoc s kódováním:**
- "Pomoz mi napsat Python kód pro připojení k CosmosDB"
- "Ukáž mi, jak vytvořit Azure Function"

**Dotazy více agentů:**
- "Začínám jako cloudový inženýr. S kým bych se měl spojit a co bych se měl naučit?"

## Struktura projektu

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

## Workflow s více agenty

Hostovaný agent používá **HandoffBuilder** k orchestraci čtyř specializovaných agentů:

| Agent | Role | Nástroje |
|-------|------|----------|
| **Triage Agent** | Koordinátor - směruje dotazy specialistům | Žádné |
| **Employee Search Agent** | Najde kolegy a členy týmu | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Vytváří vzdělávací cesty a doporučení | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generuje ukázky kódu a rady | Žádné |

Workflow umožňuje:
- Triage → Jakýkoli specialista
- Specialisté → Jiní specialisté (pro související dotazy)
- Specialisté → Triage (pro nová témata)

## Řešení problémů

### Agent neodpovídá
- Ověřte, že hostovaný agent je nasazený a běží v Azure AI Foundry
- Zkontrolujte, zda `HOSTED_AGENT_NAME` a `HOSTED_AGENT_VERSION` odpovídají vašemu nasazení

### Chyby Vector Store
- Ujistěte se, že `VECTOR_STORE_ID` je správně nastaveno
- Ověřte, že vector store obsahuje data zaměstnanců

### Chyby autentizace
- Spusťte `az login` pro obnovení přihlašovacích údajů
- Ujistěte se, že máte přístup k projektu Azure AI Foundry

## Zdroje

- [Dokumentace Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Ukázka integrace ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o vyloučení odpovědnosti**:  
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro důležité informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoliv nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->