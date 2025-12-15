<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:21:09+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "et"
}
-->
# Õppetund 4: Agendi juurutamine Azure AI Foundry hostitud agentidega + ChatKit

See õppetund demonstreerib, kuidas juurutada mitme agendiga töövoog Azure AI Foundry'sse hostitud agendina ja luua ChatKit-põhine kasutajaliides sellega suhtlemiseks.

## Arhitektuur

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

## Eeltingimused

1. **Azure AI Foundry projekt** North Central US piirkonnas
2. **Azure CLI** autentitud (`az login`)
3. **Azure Developer CLI** (`azd`) paigaldatud
4. **Python 3.12+** ja **Node.js 18+**
5. **Vektorpood** loodud töötajate andmetega

## Kiire algus

### 1. Keskkonnamuutujate seadistamine

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Muuda .env oma Azure AI Foundry projekti andmetega
```

### 2. Hostitud agendi juurutamine

**Variant A: Azure Developer CLI kasutamine (soovitatav)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Variant B: Docker + Azure Container Registry kasutamine**

```bash
cd hosted-agent

# Koosta konteiner
docker build -t developer-onboarding-agent:latest .

# Silt ACR-ile
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Lükka ACR-i
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Paigalda Azure AI Foundry portaali või SDK kaudu
```

### 3. ChatKit taustaprogrammi käivitamine

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windowsis: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server käivitub aadressil `http://localhost:8001`

### 4. ChatKit kasutajaliidese käivitamine

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Kasutajaliides käivitub aadressil `http://localhost:3000`

### 5. Rakenduse testimine

Ava brauseris `http://localhost:3000` ja proovi järgmisi päringuid:

**Töötajate otsing:**
- "Olen siin uus! Kas keegi on töötanud Microsoftis?"
- "Kellel on kogemusi Azure Functionsiga?"

**Õppematerjalid:**
- "Loo õppeteek Kuberneteseks"
- "Milliseid sertifikaate peaksin pilvearhitektuuri jaoks taotlema?"

**Koodiabi:**
- "Aita mul kirjutada Python kood CosmosDB-ga ühendamiseks"
- "Näita, kuidas luua Azure Function"

**Mitme agendi päringud:**
- "Alustan pilveinsenerina. Kellega peaksin ühendust võtma ja mida õppima?"

## Projekti struktuur

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

## Mitme agendi töövoog

Hostitud agent kasutab **HandoffBuilderit**, et koordineerida nelja spetsialiseeritud agenti:

| Agent | Roll | Tööriistad |
|-------|------|------------|
| **Triage Agent** | Koordinaator - suunab päringud spetsialistidele | Puudub |
| **Employee Search Agent** | Leiab kolleege ja meeskonnaliikmeid | HostedFileSearchTool (Vektorpood) |
| **Learning Agent** | Loob õppeteid ja soovitusi | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Genereerib koodinäiteid ja juhiseid | Puudub |

Töövoog võimaldab:
- Triage → ükskõik milline spetsialist
- Spetsialistid → teised spetsialistid (seotud päringute puhul)
- Spetsialistid → Triage (uute teemade puhul)

## Tõrkeotsing

### Agent ei vasta
- Kontrolli, et hostitud agent on juurutatud ja töötab Azure AI Foundry's
- Kontrolli, et `HOSTED_AGENT_NAME` ja `HOSTED_AGENT_VERSION` vastavad sinu juurutusele

### Vektorpoodi vead
- Veendu, et `VECTOR_STORE_ID` on õigesti seadistatud
- Kontrolli, et vektorpood sisaldab töötajate andmeid

### Autentimisvead
- Käivita `az login`, et värskendada mandaate
- Veendu, et sul on ligipääs Azure AI Foundry projektile

## Ressursid

- [Azure AI Foundry hostitud agentide dokumentatsioon](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit integratsiooni näidis](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastutusest loobumine**:
See dokument on tõlgitud kasutades tehisintellektil põhinevat tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi püüame tagada täpsust, palun arvestage, et automaatsed tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlke kasutamisest tulenevate arusaamatuste või valesti mõistmiste eest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->