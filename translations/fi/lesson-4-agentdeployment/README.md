<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:07:57+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "fi"
}
-->
# Oppitunti 4: Agentin käyttöönotto Azure AI Foundry -isännöidyillä agenteilla + ChatKit

Tässä oppitunnissa näytetään, miten moniagenttityönkulku otetaan käyttöön Azure AI Foundryssa isännöitynä agenttina ja luodaan ChatKit-pohjainen käyttöliittymä sen kanssa vuorovaikutukseen.

## Arkkitehtuuri

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

## Esivaatimukset

1. **Azure AI Foundry -projekti** North Central US -alueella
2. **Azure CLI** todennettu (`az login`)
3. **Azure Developer CLI** (`azd`) asennettuna
4. **Python 3.12+** ja **Node.js 18+**
5. **Vector Store** luotu työntekijätiedoilla

## Nopeasti käyntiin

### 1. Määritä ympäristömuuttujat

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Muokkaa .env tiedostoa Azure AI Foundry -projektisi tiedoilla
```

### 2. Ota isännöity agentti käyttöön

**Vaihtoehto A: Azure Developer CLI:n käyttö (suositeltu)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Vaihtoehto B: Docker + Azure Container Registry**

```bash
cd hosted-agent

# Rakenna kontti
docker build -t developer-onboarding-agent:latest .

# Tunniste ACR:lle
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Työnnä ACR:ään
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Ota käyttöön Azure AI Foundry -portaalin tai SDK:n kautta
```

### 3. Käynnistä ChatKit-taustapalvelin

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windowsilla: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Palvelin käynnistyy osoitteessa `http://localhost:8001`

### 4. Käynnistä ChatKit-käyttöliittymä

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Käyttöliittymä käynnistyy osoitteessa `http://localhost:3000`

### 5. Testaa sovellus

Avaa `http://localhost:3000` selaimessasi ja kokeile näitä kyselyjä:

**Työntekijähaku:**
- "Olen uusi täällä! Onko kukaan työskennellyt Microsoftilla?"
- "Kuka on kokenut Azure Functions -palveluissa?"

**Oppimateriaalit:**
- "Luo oppimispolku Kubernetesille"
- "Mitä sertifikaatteja minun pitäisi hankkia pilviarkkitehtuurin alalla?"

**Koodausapu:**
- "Auta minua kirjoittamaan Python-koodi CosmosDB-yhteyteen"
- "Näytä, miten luodaan Azure Function"

**Moniagenttikyselyt:**
- "Aloitan pilvi-insinöörinä. Kenen kanssa minun pitäisi olla yhteydessä ja mitä minun pitäisi oppia?"

## Projektin rakenne

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

## Moniagenttityönkulku

Isännöity agentti käyttää **HandoffBuilderia** neljän erikoistuneen agentin orkestrointiin:

| Agentti | Rooli | Työkalut |
|---------|-------|----------|
| **Triage Agent** | Koordinaattori - ohjaa kyselyt asiantuntijoille | Ei mitään |
| **Employee Search Agent** | Löytää kollegat ja tiimin jäsenet | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Luo oppimispolkuja ja suosituksia | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Tuottaa koodiesimerkkejä ja ohjeita | Ei mitään |

Työnkulku sallii:
- Triage → Mikä tahansa asiantuntija
- Asiantuntijat → Muut asiantuntijat (aiheeseen liittyvät kyselyt)
- Asiantuntijat → Triage (uusille aiheille)

## Vianmääritys

### Agentti ei vastaa
- Varmista, että isännöity agentti on otettu käyttöön ja käynnissä Azure AI Foundryssa
- Tarkista, että `HOSTED_AGENT_NAME` ja `HOSTED_AGENT_VERSION` vastaavat käyttöönottoasi

### Vector store -virheet
- Varmista, että `VECTOR_STORE_ID` on asetettu oikein
- Tarkista, että vector store sisältää työntekijätiedot

### Todennusvirheet
- Suorita `az login` päivittääksesi tunnistetiedot
- Varmista, että sinulla on pääsy Azure AI Foundry -projektiin

## Resurssit

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattikäännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää virallisena lähteenä. Tärkeiden tietojen osalta suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->