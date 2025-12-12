<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:51:14+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ru"
}
-->
# Урок 4: Развертывание агента с помощью Azure AI Foundry Hosted Agents + ChatKit

В этом уроке показано, как развернуть многозадачный рабочий процесс в Azure AI Foundry в виде размещённого агента и создать фронтенд на основе ChatKit для взаимодействия с ним.

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

## Требования

1. **Проект Azure AI Foundry** в регионе North Central US
2. **Azure CLI** с аутентификацией (`az login`)
3. Установленный **Azure Developer CLI** (`azd`)
4. **Python 3.12+** и **Node.js 18+**
5. Создан **Vector Store** с данными сотрудников

## Быстрый старт

### 1. Настройка переменных окружения

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Отредактируйте .env с деталями вашего проекта Azure AI Foundry
```

### 2. Развертывание размещённого агента

**Вариант A: Использование Azure Developer CLI (рекомендуется)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Вариант B: Использование Docker + Azure Container Registry**

```bash
cd hosted-agent

# Собрать контейнер
docker build -t developer-onboarding-agent:latest .

# Тег для ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Отправить в ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Развернуть через портал Azure AI Foundry или SDK
```

### 3. Запуск бэкенда ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # В Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Сервер запустится по адресу `http://localhost:8001`

### 4. Запуск фронтенда ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Фронтенд запустится по адресу `http://localhost:3000`

### 5. Тестирование приложения

Откройте `http://localhost:3000` в браузере и попробуйте следующие запросы:

**Поиск сотрудников:**
- "Я здесь новенький! Кто-нибудь работал в Microsoft?"
- "Кто имеет опыт работы с Azure Functions?"

**Обучающие ресурсы:**
- "Создай учебный план по Kubernetes"
- "Какие сертификаты стоит получить для облачной архитектуры?"

**Помощь с кодированием:**
- "Помоги написать Python-код для подключения к CosmosDB"
- "Покажи, как создать Azure Function"

**Запросы к нескольким агентам:**
- "Я начинаю как облачный инженер. С кем мне связаться и что изучать?"

## Структура проекта

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

## Многозадачный рабочий процесс

Размещённый агент использует **HandoffBuilder** для координации четырёх специализированных агентов:

| Агент | Роль | Инструменты |
|-------|------|-------------|
| **Triage Agent** | Координатор — направляет запросы специалистам | Нет |
| **Employee Search Agent** | Находит коллег и членов команды | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Создаёт учебные планы и рекомендации | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Генерирует примеры кода и рекомендации | Нет |

Рабочий процесс позволяет:
- Triage → Любому специалисту
- Специалистам → Другим специалистам (по смежным вопросам)
- Специалистам → Triage (по новым темам)

## Устранение неполадок

### Агент не отвечает
- Проверьте, что размещённый агент развернут и запущен в Azure AI Foundry
- Убедитесь, что `HOSTED_AGENT_NAME` и `HOSTED_AGENT_VERSION` соответствуют вашей развертке

### Ошибки в Vector Store
- Убедитесь, что `VECTOR_STORE_ID` установлен правильно
- Проверьте, что в векторном хранилище содержатся данные сотрудников

### Ошибки аутентификации
- Выполните `az login` для обновления учётных данных
- Убедитесь, что у вас есть доступ к проекту Azure AI Foundry

## Ресурсы

- [Документация Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Пример интеграции ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия обеспечить точность, имейте в виду, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обращаться к профессиональному переводу, выполненному человеком. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования данного перевода.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->