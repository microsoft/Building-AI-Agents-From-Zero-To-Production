<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:19:48+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "lt"
}
-->
# 4 pamoka: Agentų diegimas naudojant Azure AI Foundry talpinamus agentus + ChatKit

Šioje pamokoje demonstruojama, kaip diegti daugiagentinį darbo eigą į Azure AI Foundry kaip talpinamą agentą ir sukurti ChatKit pagrindu veikiantį frontendą sąveikai su juo.

## Architektūra

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

## Išankstiniai reikalavimai

1. **Azure AI Foundry projektas** Šiaurės Centrinės JAV regione
2. **Azure CLI** autentifikuotas (`az login`)
3. Įdiegta **Azure Developer CLI** (`azd`)
4. **Python 3.12+** ir **Node.js 18+**
5. Sukurtas **vektorinės saugyklos** su darbuotojų duomenimis

## Greitas pradėjimas

### 1. Nustatykite aplinkos kintamuosius

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Redaguokite .env su savo Azure AI Foundry projekto duomenimis
```

### 2. Diegti talpinamą agentą

**A variantas: naudojant Azure Developer CLI (rekomenduojama)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**B variantas: naudojant Docker + Azure Container Registry**

```bash
cd hosted-agent

# Sukurti konteinerį
docker build -t developer-onboarding-agent:latest .

# Žyma ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Įkelti į ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Diegti per Azure AI Foundry portalą arba SDK
```

### 3. Paleiskite ChatKit backendą

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows sistemoje: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Serveris pradės veikti adresu `http://localhost:8001`

### 4. Paleiskite ChatKit frontendą

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend pradės veikti adresu `http://localhost:3000`

### 5. Išbandykite programą

Atidarykite `http://localhost:3000` naršyklėje ir išbandykite šiuos užklausimus:

**Darbuotojų paieška:**
- „Aš čia naujas! Ar kas nors dirbo Microsoft?“
- „Kas turi patirties su Azure Functions?“

**Mokymosi ištekliai:**
- „Sukurk mokymosi kelią Kubernetes“
- „Kokias sertifikacijas turėčiau siekti debesų architektūrai?“

**Kodo pagalba:**
- „Padėk man parašyti Python kodą prisijungimui prie CosmosDB“
- „Parodyk, kaip sukurti Azure Function“

**Daugiagentinės užklausos:**
- „Pradedu kaip debesų inžinierius. Su kuo turėčiau susisiekti ir ką turėčiau išmokti?“

## Projekto struktūra

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

## Daugiagentinė darbo eiga

Talpinamas agentas naudoja **HandoffBuilder**, kad koordinuotų keturis specializuotus agentus:

| Agentas | Vaidmuo | Įrankiai |
|---------|---------|----------|
| **Triage agentas** | Koordinatorius – nukreipia užklausas specialistams | Nėra |
| **Darbuotojų paieškos agentas** | Randa kolegas ir komandos narius | HostedFileSearchTool (vektorinė saugykla) |
| **Mokymosi agentas** | Kuria mokymosi kelius ir rekomendacijas | HostedMCPTool (Microsoft Learn) |
| **Kodo agentas** | Generuoja kodo pavyzdžius ir patarimus | Nėra |

Darbo eiga leidžia:
- Triage → bet kuris specialistas
- Specialistai → kiti specialistai (susijusioms užklausoms)
- Specialistai → Triage (naujoms temoms)

## Trikčių šalinimas

### Agentas neatsako
- Patikrinkite, ar talpinamas agentas yra įdiegtas ir veikia Azure AI Foundry
- Patikrinkite, ar `HOSTED_AGENT_NAME` ir `HOSTED_AGENT_VERSION` atitinka jūsų diegimą

### Vektorinės saugyklos klaidos
- Įsitikinkite, kad `VECTOR_STORE_ID` nustatytas teisingai
- Patikrinkite, ar vektorinė saugykla turi darbuotojų duomenis

### Autentifikacijos klaidos
- Paleiskite `az login`, kad atnaujintumėte kredencialus
- Įsitikinkite, kad turite prieigą prie Azure AI Foundry projekto

## Ištekliai

- [Azure AI Foundry talpinamų agentų dokumentacija](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft agentų sistema](https://github.com/microsoft/agent-framework)
- [ChatKit integracijos pavyzdys](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas jo gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojamas profesionalus žmogaus vertimas. Mes neatsakome už bet kokius nesusipratimus ar neteisingus aiškinimus, kilusius dėl šio vertimo naudojimo.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->