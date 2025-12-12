<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:15:34+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "bg"
}
-->
# Lesson 4: Разгръщане на агент с Azure AI Foundry Hosted Agents + ChatKit

Този урок демонстрира как да разположите мултиагентен работен процес в Azure AI Foundry като хостван агент и да създадете фронтенд базиран на ChatKit за взаимодействие с него.

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

## Предварителни изисквания

1. **Проект в Azure AI Foundry** в региона North Central US
2. **Azure CLI** с удостоверяване (`az login`)
3. **Azure Developer CLI** (`azd`) инсталиран
4. **Python 3.12+** и **Node.js 18+**
5. **Vector Store** създаден с данни за служителите

## Бърз старт

### 1. Настройване на променливи на средата

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Редактирайте .env с детайлите на вашия проект Azure AI Foundry
```

### 2. Разгръщане на хоствания агент

**Опция A: Използване на Azure Developer CLI (Препоръчително)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Опция B: Използване на Docker + Azure Container Registry**

```bash
cd hosted-agent

# Изградете контейнера
docker build -t developer-onboarding-agent:latest .

# Таг за ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Качване в ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Разгръщане чрез портала Azure AI Foundry или SDK
```

### 3. Стартиране на ChatKit бекенда

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # В Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Сървърът ще стартира на `http://localhost:8001`

### 4. Стартиране на ChatKit фронтенда

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Фронтендът ще стартира на `http://localhost:3000`

### 5. Тествайте приложението

Отворете `http://localhost:3000` в браузъра си и опитайте следните заявки:

**Търсене на служител:**
- "Аз съм нов тук! Някой работил ли е в Microsoft?"
- "Кой има опит с Azure Functions?"

**Обучителни ресурси:**
- "Създай учебен път за Kubernetes"
- "Какви сертификати трябва да взема за облачна архитектура?"

**Помощ с кодиране:**
- "Помогни ми да напиша Python код за свързване с CosmosDB"
- "Покажи ми как да създам Azure Function"

**Мултиагентни заявки:**
- "Започвам като облачен инженер. С кого трябва да се свържа и какво да науча?"

## Структура на проекта

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

## Мултиагентният работен процес

Хостваният агент използва **HandoffBuilder** за оркестрация на четири специализирани агенти:

| Агент | Роля | Инструменти |
|-------|------|-------------|
| **Triage Agent** | Координатор - насочва заявките към специалисти | Няма |
| **Employee Search Agent** | Намира колеги и членове на екипа | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Създава учебни пътеки и препоръки | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Генерира кодови примери и насоки | Няма |

Работният процес позволява:
- Triage → Всеки специалист
- Специалисти → Други специалисти (за свързани заявки)
- Специалисти → Triage (за нови теми)

## Отстраняване на проблеми

### Агентът не отговаря
- Проверете дали хостваният агент е разположен и работи в Azure AI Foundry
- Проверете дали `HOSTED_AGENT_NAME` и `HOSTED_AGENT_VERSION` съвпадат с вашето разгръщане

### Грешки с Vector store
- Уверете се, че `VECTOR_STORE_ID` е зададен правилно
- Проверете дали vector store съдържа данните за служителите

### Грешки при удостоверяване
- Изпълнете `az login`, за да обновите удостоверенията
- Уверете се, че имате достъп до проекта в Azure AI Foundry

## Ресурси

- [Документация за Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Пример за интеграция с ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от отговорност**:
Този документ е преведен с помощта на AI преводаческа услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->