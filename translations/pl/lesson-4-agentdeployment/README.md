<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:03:08+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "pl"
}
-->
# Lekcja 4: Wdrażanie agenta z Azure AI Foundry Hosted Agents + ChatKit

Ta lekcja pokazuje, jak wdrożyć wieloagentowy przepływ pracy do Azure AI Foundry jako hostowanego agenta oraz jak stworzyć frontend oparty na ChatKit do interakcji z nim.

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

## Wymagania wstępne

1. **Projekt Azure AI Foundry** w regionie North Central US
2. **Azure CLI** uwierzytelnione (`az login`)
3. **Azure Developer CLI** (`azd`) zainstalowane
4. **Python 3.12+** oraz **Node.js 18+**
5. **Vector Store** utworzony z danymi pracowników

## Szybki start

### 1. Ustaw zmienne środowiskowe

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edytuj plik .env, wpisując szczegóły swojego projektu Azure AI Foundry
```

### 2. Wdróż hostowanego agenta

**Opcja A: Użycie Azure Developer CLI (zalecane)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opcja B: Użycie Docker + Azure Container Registry**

```bash
cd hosted-agent

# Zbuduj kontener
docker build -t developer-onboarding-agent:latest .

# Tag dla ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Wypchnij do ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Wdróż za pomocą portalu Azure AI Foundry lub SDK
```

### 3. Uruchom backend ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # W systemie Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Serwer uruchomi się pod adresem `http://localhost:8001`

### 4. Uruchom frontend ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend uruchomi się pod adresem `http://localhost:3000`

### 5. Przetestuj aplikację

Otwórz `http://localhost:3000` w przeglądarce i wypróbuj następujące zapytania:

**Wyszukiwanie pracowników:**
- "Jestem tu nowy! Czy ktoś pracował w Microsoft?"
- "Kto ma doświadczenie z Azure Functions?"

**Zasoby edukacyjne:**
- "Stwórz ścieżkę nauki dla Kubernetes"
- "Jakie certyfikaty powinienem zdobyć, aby zostać architektem chmury?"

**Pomoc w kodowaniu:**
- "Pomóż mi napisać kod w Pythonie do połączenia z CosmosDB"
- "Pokaż, jak stworzyć Azure Function"

**Zapytania wieloagentowe:**
- "Zaczynam jako inżynier chmury. Z kim powinienem się skontaktować i czego się uczyć?"

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

## Wieloagentowy przepływ pracy

Hostowany agent używa **HandoffBuilder** do koordynacji czterech wyspecjalizowanych agentów:

| Agent | Rola | Narzędzia |
|-------|------|-----------|
| **Agent triage** | Koordynator - kieruje zapytania do specjalistów | Brak |
| **Agent wyszukiwania pracowników** | Znajduje współpracowników i członków zespołu | HostedFileSearchTool (Vector Store) |
| **Agent edukacyjny** | Tworzy ścieżki nauki i rekomendacje | HostedMCPTool (Microsoft Learn) |
| **Agent kodujący** | Generuje przykłady kodu i wskazówki | Brak |

Przepływ pracy pozwala na:
- Triage → dowolny specjalista
- Specjaliści → inni specjaliści (dla powiązanych zapytań)
- Specjaliści → Triage (dla nowych tematów)

## Rozwiązywanie problemów

### Agent nie odpowiada
- Sprawdź, czy hostowany agent jest wdrożony i działa w Azure AI Foundry
- Zweryfikuj, czy `HOSTED_AGENT_NAME` i `HOSTED_AGENT_VERSION` odpowiadają Twojemu wdrożeniu

### Błędy Vector Store
- Upewnij się, że `VECTOR_STORE_ID` jest poprawnie ustawione
- Sprawdź, czy vector store zawiera dane pracowników

### Błędy uwierzytelniania
- Uruchom `az login`, aby odświeżyć poświadczenia
- Upewnij się, że masz dostęp do projektu Azure AI Foundry

## Zasoby

- [Dokumentacja Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Przykład integracji ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mimo że dokładamy starań, aby tłumaczenie było jak najbardziej precyzyjne, prosimy mieć na uwadze, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w języku źródłowym powinien być uznawany za źródło autorytatywne. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->