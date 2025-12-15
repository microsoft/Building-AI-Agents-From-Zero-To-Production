<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:16:12+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "sr"
}
-->
# Lesson 4: Распоређивање агента са Azure AI Foundry Hosted Agents + ChatKit

Ова лекција показује како да распоредите мулти-агентски ток рада у Azure AI Foundry као хостованог агента и креирате ChatKit-базирани фронтенд за интеракцију са њим.

## Архитектура

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

## Предуслови

1. **Azure AI Foundry пројекат** у региону North Central US
2. **Azure CLI** аутентификован (`az login`)
3. **Azure Developer CLI** (`azd`) инсталиран
4. **Python 3.12+** и **Node.js 18+**
5. **Vector Store** креиран са подацима о запосленима

## Брзи почетак

### 1. Подешавање променљивих окружења

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Уредите .env са детаљима вашег Azure AI Foundry пројекта
```

### 2. Распоређивање хостованог агента

**Опција А: Коришћење Azure Developer CLI (препоручено)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Опција Б: Коришћење Docker + Azure Container Registry**

```bash
cd hosted-agent

# Изградите контејнер
docker build -t developer-onboarding-agent:latest .

# Ознака за ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Пошаљите у ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Деплој преко Azure AI Foundry портала или SDK-а
```

### 3. Покретање ChatKit бекенда

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # На Виндоус-у: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Сервер ће се покренути на `http://localhost:8001`

### 4. Покретање ChatKit фронтенда

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Фронтенд ће се покренути на `http://localhost:3000`

### 5. Тестирање апликације

Отворите `http://localhost:3000` у вашем прегледачу и испробајте ове упите:

**Претрага запослених:**
- "Ја сам нов овде! Да ли је неко радио у Microsoft-у?"
- "Ко има искуство са Azure Functions?"

**Ресурси за учење:**
- "Креирај пут учења за Kubernetes"
- "Које сертификате треба да стекнем за облачну архитектуру?"

**Помоћ око кодирања:**
- "Помози ми да напишем Python код за повезивање са CosmosDB"
- "Покажи ми како да направим Azure Function"

**Мулти-агентски упити:**
- "Почињем као cloud инжењер. Са ким треба да се повежем и шта треба да учим?"

## Структура пројекта

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

## Мулти-агентски ток рада

Хостовани агент користи **HandoffBuilder** за оркестрацију четири специјализована агента:

| Агент | Улога | Алати |
|-------|-------|-------|
| **Triage Agent** | Координатор - усмерава упите специјалистима | Ниједан |
| **Employee Search Agent** | Проналази колеге и чланове тима | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Креира путеве учења и препоруке | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Генерише примере кода и смернице | Ниједан |

Ток рада дозвољава:
- Triage → било који специјалиста
- Специјалисти → други специјалисти (за повезане упите)
- Специјалисти → Triage (за нове теме)

## Решавање проблема

### Агент не одговара
- Проверите да ли је хостовани агент распоређен и покренут у Azure AI Foundry
- Проверите да ли `HOSTED_AGENT_NAME` и `HOSTED_AGENT_VERSION` одговарају вашем распоређивању

### Грешке везане за vector store
- Уверите се да је `VECTOR_STORE_ID` исправно подешен
- Проверите да ли vector store садржи податке о запосленима

### Грешке аутентификације
- Покрените `az login` да освежите акредитиве
- Уверите се да имате приступ Azure AI Foundry пројекту

## Ресурси

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Одрицање од одговорности**:
Овај документ је преведен коришћењем AI услуге за превођење [Co-op Translator](https://github.com/Azure/co-op-translator). Иако се трудимо да превод буде тачан, имајте у виду да аутоматски преводи могу садржати грешке или нетачности. Оригинални документ на његовом изворном језику треба сматрати ауторитетним извором. За критичне информације препоручује се професионални људски превод. Нисмо одговорни за било каква неспоразума или погрешна тумачења која произилазе из коришћења овог превода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->