<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:19:08+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "uk"
}
-->
# Урок 4: Розгортання агента з Azure AI Foundry Hosted Agents + ChatKit

У цьому уроці показано, як розгорнути багатофункціональний робочий процес агента в Azure AI Foundry як розміщеного агента та створити фронтенд на основі ChatKit для взаємодії з ним.

## Архітектура

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

## Вимоги

1. **Проєкт Azure AI Foundry** у регіоні North Central US
2. **Azure CLI** з автентифікацією (`az login`)
3. Встановлений **Azure Developer CLI** (`azd`)
4. **Python 3.12+** та **Node.js 18+**
5. Створений **Vector Store** з даними працівників

## Швидкий старт

### 1. Налаштуйте змінні середовища

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Відредагуйте .env з деталями вашого проекту Azure AI Foundry
```

### 2. Розгорніть розміщеного агента

**Варіант A: Використання Azure Developer CLI (рекомендовано)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Варіант B: Використання Docker + Azure Container Registry**

```bash
cd hosted-agent

# Зібрати контейнер
docker build -t developer-onboarding-agent:latest .

# Тег для ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Відправити в ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Розгорнути через портал Azure AI Foundry або SDK
```

### 3. Запустіть бекенд ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # У Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Сервер запуститься за адресою `http://localhost:8001`

### 4. Запустіть фронтенд ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Фронтенд запуститься за адресою `http://localhost:3000`

### 5. Перевірте застосунок

Відкрийте `http://localhost:3000` у браузері та спробуйте ці запити:

**Пошук працівників:**
- "Я новачок тут! Хтось працював у Microsoft?"
- "Хто має досвід з Azure Functions?"

**Навчальні ресурси:**
- "Створіть навчальний шлях для Kubernetes"
- "Які сертифікати мені слід отримати для архітектури хмар?"

**Допомога з кодуванням:**
- "Допоможіть написати Python-код для підключення до CosmosDB"
- "Покажіть, як створити Azure Function"

**Запити багатьом агентам:**
- "Я починаю як інженер хмар. З ким мені варто зв’язатися і що вивчати?"

## Структура проєкту

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

## Багатофункціональний робочий процес агента

Розміщений агент використовує **HandoffBuilder** для координації чотирьох спеціалізованих агентів:

| Агент | Роль | Інструменти |
|-------|------|-------------|
| **Triage Agent** | Координатор - направляє запити до спеціалістів | Відсутні |
| **Employee Search Agent** | Знаходить колег і членів команди | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Створює навчальні шляхи та рекомендації | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Генерує приклади коду та рекомендації | Відсутні |

Робочий процес дозволяє:
- Triage → будь-якому спеціалісту
- Спеціалісти → іншим спеціалістам (для суміжних запитів)
- Спеціалісти → Triage (для нових тем)

## Вирішення проблем

### Агент не відповідає
- Перевірте, чи розміщений агент розгорнутий і працює в Azure AI Foundry
- Переконайтеся, що `HOSTED_AGENT_NAME` та `HOSTED_AGENT_VERSION` відповідають вашому розгортанню

### Помилки Vector Store
- Переконайтеся, що `VECTOR_STORE_ID` встановлено правильно
- Перевірте, чи містить vector store дані працівників

### Помилки автентифікації
- Виконайте `az login` для оновлення облікових даних
- Переконайтеся, що у вас є доступ до проєкту Azure AI Foundry

## Ресурси

- [Документація Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Приклад інтеграції ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Відмова від відповідальності**:
Цей документ було перекладено за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується звертатися до професійного людського перекладу. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->