<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:12:51+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "hu"
}
-->
# 4. Lecke: Ügynök telepítése Azure AI Foundry hosztolt ügynökökkel + ChatKit

Ez a lecke bemutatja, hogyan lehet egy többügynökös munkafolyamatot telepíteni az Azure AI Foundry-ba hosztolt ügynökként, és létrehozni egy ChatKit-alapú frontend felületet a vele való interakcióhoz.

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

## Előfeltételek

1. **Azure AI Foundry projekt** a North Central US régióban
2. **Azure CLI** hitelesítve (`az login`)
3. **Azure Developer CLI** (`azd`) telepítve
4. **Python 3.12+** és **Node.js 18+**
5. **Vektor tároló** létrehozva alkalmazotti adatokkal

## Gyors kezdés

### 1. Környezeti változók beállítása

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Szerkessze a .env fájlt az Azure AI Foundry projekt részleteivel
```

### 2. A hosztolt ügynök telepítése

**A lehetőség: Azure Developer CLI használata (ajánlott)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**B lehetőség: Docker + Azure Container Registry használata**

```bash
cd hosted-agent

# A konténer építése
docker build -t developer-onboarding-agent:latest .

# Címke az ACR-hez
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Feltöltés az ACR-be
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Telepítés az Azure AI Foundry portálon vagy SDK-n keresztül
```

### 3. A ChatKit backend indítása

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows rendszeren: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

A szerver a `http://localhost:8001` címen fog elindulni

### 4. A ChatKit frontend indítása

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

A frontend a `http://localhost:3000` címen fog elindulni

### 5. Az alkalmazás tesztelése

Nyisd meg a `http://localhost:3000` oldalt a böngésződben, és próbáld ki ezeket a lekérdezéseket:

**Alkalmazotti keresés:**
- "Új vagyok itt! Dolgozott már valaki a Microsoftnál?"
- "Kinek van tapasztalata az Azure Functions használatában?"

**Tanulási források:**
- "Készíts egy tanulási útvonalat Kuberneteshez"
- "Milyen tanúsítványokat érdemes szereznem felhőarchitektúrához?"

**Kódolási segítség:**
- "Segíts Python kódot írni CosmosDB-hez való kapcsolódáshoz"
- "Mutasd meg, hogyan készíthetek Azure Function-t"

**Többügynökös lekérdezések:**
- "Felhőmérnökként kezdek. Kivel érdemes kapcsolatba lépnem és mit tanuljak?"

## Projekt struktúra

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

## A többügynökös munkafolyamat

A hosztolt ügynök a **HandoffBuilder**-t használja négy specializált ügynök összehangolására:

| Ügynök | Szerep | Eszközök |
|--------|--------|----------|
| **Triage Agent** | Koordinátor - a lekérdezéseket szakértőkhöz irányítja | Nincs |
| **Employee Search Agent** | Kollégák és csapattagok keresése | HostedFileSearchTool (Vektor tároló) |
| **Learning Agent** | Tanulási utak és ajánlások készítése | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Kódminták és útmutatás generálása | Nincs |

A munkafolyamat lehetővé teszi:
- Triage → Bármely szakértő
- Szakértők → Más szakértők (kapcsolódó lekérdezésekhez)
- Szakértők → Triage (új témákhoz)

## Hibakeresés

### Az ügynök nem válaszol
- Ellenőrizd, hogy a hosztolt ügynök telepítve és fut az Azure AI Foundry-ban
- Ellenőrizd, hogy a `HOSTED_AGENT_NAME` és `HOSTED_AGENT_VERSION` megegyezik a telepítéseddel

### Vektor tároló hibák
- Győződj meg róla, hogy a `VECTOR_STORE_ID` helyesen van beállítva
- Ellenőrizd, hogy a vektor tároló tartalmazza az alkalmazotti adatokat

### Hitelesítési hibák
- Futtasd az `az login` parancsot a hitelesítő adatok frissítéséhez
- Győződj meg róla, hogy hozzáférsz az Azure AI Foundry projekthez

## Források

- [Azure AI Foundry hosztolt ügynökök dokumentációja](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit integrációs példa](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ezt a dokumentumot az AI fordító szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével fordítottuk le. Bár a pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén szakmai, emberi fordítást javaslunk. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy félreértelmezésekért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->