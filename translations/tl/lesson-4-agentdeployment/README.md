<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:11:28+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "tl"
}
-->
# Lesson 4: Pag-deploy ng Ahente gamit ang Azure AI Foundry Hosted Agents + ChatKit

Ipinapakita ng leksyon na ito kung paano mag-deploy ng multi-agent workflow sa Azure AI Foundry bilang hosted agent at gumawa ng ChatKit-based frontend upang makipag-ugnayan dito.

## Arkitektura

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

## Mga Kinakailangan

1. **Azure AI Foundry Project** sa rehiyon ng North Central US
2. **Azure CLI** na naka-authenticate (`az login`)
3. **Azure Developer CLI** (`azd`) na naka-install
4. **Python 3.12+** at **Node.js 18+**
5. **Vector Store** na nilikha gamit ang data ng empleyado

## Mabilisang Pagsisimula

### 1. I-set Up ang Mga Environment Variables

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# I-edit ang .env gamit ang mga detalye ng iyong Azure AI Foundry na proyekto
```

### 2. I-deploy ang Hosted Agent

**Opsyon A: Paggamit ng Azure Developer CLI (Inirerekomenda)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opsyon B: Paggamit ng Docker + Azure Container Registry**

```bash
cd hosted-agent

# Itayo ang lalagyan
docker build -t developer-onboarding-agent:latest .

# Tag para sa ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Itulak sa ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# I-deploy sa pamamagitan ng Azure AI Foundry portal o SDK
```

### 3. Simulan ang ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Sa Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Magsisimula ang server sa `http://localhost:8001`

### 4. Simulan ang ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Magsisimula ang frontend sa `http://localhost:3000`

### 5. Subukan ang Aplikasyon

Buksan ang `http://localhost:3000` sa iyong browser at subukan ang mga sumusunod na tanong:

**Paghahanap ng Empleyado:**
- "Bago ako dito! May nakatrabaho na ba sa Microsoft?"
- "Sino ang may karanasan sa Azure Functions?"

**Mga Mapagkukunan sa Pag-aaral:**
- "Gumawa ng learning path para sa Kubernetes"
- "Anong mga sertipikasyon ang dapat kong kunin para sa cloud architecture?"

**Tulong sa Pag-coding:**
- "Tulungan mo akong magsulat ng Python code para kumonekta sa CosmosDB"
- "Ipakita mo sa akin kung paano gumawa ng Azure Function"

**Mga Tanong mula sa Maramihang Ahente:**
- "Nagsisimula ako bilang cloud engineer. Kanino ako dapat kumonekta at ano ang dapat kong pag-aralan?"

## Estruktura ng Proyekto

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

## Ang Multi-Agent Workflow

Gumagamit ang hosted agent ng **HandoffBuilder** upang pamahalaan ang apat na espesyalistang ahente:

| Ahente | Papel | Mga Kasangkapan |
|--------|-------|----------------|
| **Triage Agent** | Tagapag-ugnay - nagruruta ng mga tanong sa mga espesyalista | Wala |
| **Employee Search Agent** | Naghahanap ng mga kasamahan at miyembro ng koponan | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Gumagawa ng mga learning path at rekomendasyon | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Gumagawa ng mga halimbawa ng code at gabay | Wala |

Pinapayagan ng workflow ang:
- Triage → Anumang espesyalista
- Mga espesyalista → Ibang mga espesyalista (para sa mga kaugnay na tanong)
- Mga espesyalista → Triage (para sa mga bagong paksa)

## Pag-troubleshoot

### Hindi sumasagot ang ahente
- Siguraduhing na-deploy at tumatakbo ang hosted agent sa Azure AI Foundry
- Suriin na ang `HOSTED_AGENT_NAME` at `HOSTED_AGENT_VERSION` ay tumutugma sa iyong deployment

### Mga error sa vector store
- Siguraduhing tama ang pagkaka-set ng `VECTOR_STORE_ID`
- Tiyaking naglalaman ang vector store ng data ng empleyado

### Mga error sa authentication
- Patakbuhin ang `az login` upang i-refresh ang mga kredensyal
- Siguraduhing may access ka sa Azure AI Foundry project

## Mga Mapagkukunan

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Paunawa**:
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagamat nagsusumikap kami para sa katumpakan, pakatandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o di-tumpak na impormasyon. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na maaaring magmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->