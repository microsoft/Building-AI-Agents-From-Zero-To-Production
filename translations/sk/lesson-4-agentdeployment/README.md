<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:14:15+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "sk"
}
-->
# Lekcia 4: Nasadenie agenta s Azure AI Foundry Hosted Agents + ChatKit

Táto lekcia ukazuje, ako nasadiť viacagentový pracovný tok do Azure AI Foundry ako hostovaného agenta a vytvoriť frontend založený na ChatKit na interakciu s ním.

## Architektúra

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

## Predpoklady

1. **Projekt Azure AI Foundry** v regióne North Central US
2. **Azure CLI** autentifikovaný (`az login`)
3. **Azure Developer CLI** (`azd`) nainštalovaný
4. **Python 3.12+** a **Node.js 18+**
5. **Vektorové úložisko** vytvorené s údajmi o zamestnancoch

## Rýchly štart

### 1. Nastavte premenné prostredia

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Upravte .env so svojimi údajmi projektu Azure AI Foundry
```

### 2. Nasadte hostovaného agenta

**Možnosť A: Použitie Azure Developer CLI (odporúčané)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Možnosť B: Použitie Docker + Azure Container Registry**

```bash
cd hosted-agent

# Vytvorte kontajner
docker build -t developer-onboarding-agent:latest .

# Značka pre ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Odoslať do ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Nasadiť cez portál Azure AI Foundry alebo SDK
```

### 3. Spustite backend ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Na Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server sa spustí na `http://localhost:8001`

### 4. Spustite frontend ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend sa spustí na `http://localhost:3000`

### 5. Otestujte aplikáciu

Otvorte `http://localhost:3000` vo vašom prehliadači a vyskúšajte tieto dotazy:

**Vyhľadávanie zamestnancov:**
- "Som tu nový! Pracoval niekto v Microsoft?"
- "Kto má skúsenosti s Azure Functions?"

**Vzdelávacie zdroje:**
- "Vytvor mi učebnú cestu pre Kubernetes"
- "Aké certifikácie by som mal získať pre cloudovú architektúru?"

**Pomoc s kódovaním:**
- "Pomôž mi napísať Python kód na pripojenie k CosmosDB"
- "Ukáž mi, ako vytvoriť Azure Function"

**Viacagentové dotazy:**
- "Začínam ako cloudový inžinier. S kým by som sa mal spojiť a čo by som sa mal naučiť?"

## Štruktúra projektu

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

## Viacagentový pracovný tok

Hostovaný agent používa **HandoffBuilder** na orchestráciu štyroch špecializovaných agentov:

| Agent | Úloha | Nástroje |
|-------|-------|----------|
| **Triage Agent** | Koordinátor - smeruje dotazy k špecialistom | Žiadne |
| **Employee Search Agent** | Nájde kolegov a členov tímu | HostedFileSearchTool (Vektorové úložisko) |
| **Learning Agent** | Vytvára učebné cesty a odporúčania | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Generuje ukážky kódu a návody | Žiadne |

Pracovný tok umožňuje:
- Triage → Akýkoľvek špecialista
- Špecialisti → Iní špecialisti (pre súvisiace dotazy)
- Špecialisti → Triage (pre nové témy)

## Riešenie problémov

### Agent neodpovedá
- Overte, či je hostovaný agent nasadený a beží v Azure AI Foundry
- Skontrolujte, či `HOSTED_AGENT_NAME` a `HOSTED_AGENT_VERSION` zodpovedajú vášmu nasadeniu

### Chyby vektorového úložiska
- Uistite sa, že `VECTOR_STORE_ID` je správne nastavené
- Overte, či vektorové úložisko obsahuje údaje o zamestnancoch

### Chyby autentifikácie
- Spustite `az login` na obnovenie poverení
- Uistite sa, že máte prístup k projektu Azure AI Foundry

## Zdroje

- [Dokumentácia Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Ukážka integrácie ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:  
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, berte prosím na vedomie, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho rodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->