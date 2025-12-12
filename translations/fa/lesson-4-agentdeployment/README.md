<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:52:28+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "fa"
}
-->
# درس ۴: استقرار عامل با Azure AI Foundry Hosted Agents + ChatKit

این درس نشان می‌دهد چگونه یک جریان کاری چندعاملی را به عنوان یک عامل میزبانی شده در Azure AI Foundry مستقر کرده و یک رابط کاربری مبتنی بر ChatKit برای تعامل با آن ایجاد کنیم.

## معماری

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

## پیش‌نیازها

۱. **پروژه Azure AI Foundry** در منطقه North Central US  
۲. **Azure CLI** احراز هویت شده (`az login`)  
۳. **Azure Developer CLI** (`azd`) نصب شده  
۴. **Python 3.12+** و **Node.js 18+**  
۵. **Vector Store** ایجاد شده با داده‌های کارمندان  

## شروع سریع

### ۱. تنظیم متغیرهای محیطی

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# فایل .env را با جزئیات پروژه Azure AI Foundry خود ویرایش کنید
```

### ۲. استقرار عامل میزبانی شده

**گزینه الف: استفاده از Azure Developer CLI (توصیه شده)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**گزینه ب: استفاده از Docker + Azure Container Registry**

```bash
cd hosted-agent

# ساخت کانتینر
docker build -t developer-onboarding-agent:latest .

# برچسب برای ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ارسال به ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# استقرار از طریق پرتال Azure AI Foundry یا SDK
```

### ۳. راه‌اندازی بک‌اند ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # در ویندوز: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

سرور روی `http://localhost:8001` راه‌اندازی خواهد شد

### ۴. راه‌اندازی فرانت‌اند ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

فرانت‌اند روی `http://localhost:3000` راه‌اندازی خواهد شد

### ۵. آزمایش برنامه

آدرس `http://localhost:3000` را در مرورگر خود باز کنید و این پرسش‌ها را امتحان کنید:

**جستجوی کارمند:**  
- "من تازه‌وارد هستم! آیا کسی در مایکروسافت کار کرده است؟"  
- "چه کسی تجربه کار با Azure Functions را دارد؟"  

**منابع یادگیری:**  
- "یک مسیر یادگیری برای Kubernetes بساز"  
- "چه گواهینامه‌هایی باید برای معماری ابری دنبال کنم؟"  

**کمک برنامه‌نویسی:**  
- "کمکم کن کد پایتون برای اتصال به CosmosDB بنویسم"  
- "نشانم بده چطور یک Azure Function بسازم"  

**پرسش‌های چندعاملی:**  
- "من به عنوان مهندس ابری شروع می‌کنم. با چه کسی باید ارتباط بگیرم و چه چیزی باید یاد بگیرم؟"  

## ساختار پروژه

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

## جریان کاری چندعاملی

عامل میزبانی شده از **HandoffBuilder** برای هماهنگی چهار عامل تخصصی استفاده می‌کند:

| عامل | نقش | ابزارها |
|-------|------|-------|
| **عامل تریاژ** | هماهنگ‌کننده - هدایت پرسش‌ها به متخصصان | هیچ |
| **عامل جستجوی کارمند** | یافتن همکاران و اعضای تیم | HostedFileSearchTool (Vector Store) |
| **عامل یادگیری** | ایجاد مسیرهای یادگیری و توصیه‌ها | HostedMCPTool (Microsoft Learn) |
| **عامل برنامه‌نویسی** | تولید نمونه کد و راهنمایی | هیچ |

جریان کاری اجازه می‌دهد:  
- تریاژ → هر متخصص  
- متخصصان → سایر متخصصان (برای پرسش‌های مرتبط)  
- متخصصان → تریاژ (برای موضوعات جدید)  

## عیب‌یابی

### عامل پاسخ نمی‌دهد  
- اطمینان حاصل کنید عامل میزبانی شده در Azure AI Foundry مستقر و در حال اجرا است  
- بررسی کنید `HOSTED_AGENT_NAME` و `HOSTED_AGENT_VERSION` با استقرار شما مطابقت دارند  

### خطاهای Vector store  
- مطمئن شوید `VECTOR_STORE_ID` به درستی تنظیم شده است  
- بررسی کنید vector store شامل داده‌های کارمندان باشد  

### خطاهای احراز هویت  
- دستور `az login` را برای تازه‌سازی اعتبارنامه‌ها اجرا کنید  
- اطمینان حاصل کنید به پروژه Azure AI Foundry دسترسی دارید  

## منابع

- [مستندات Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)  
- [چارچوب عامل مایکروسافت](https://github.com/microsoft/agent-framework)  
- [نمونه ادغام ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)  
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**سلب مسئولیت**:  
این سند با استفاده از سرویس ترجمه هوش مصنوعی [Co-op Translator](https://github.com/Azure/co-op-translator) ترجمه شده است. در حالی که ما در تلاش برای دقت هستیم، لطفاً توجه داشته باشید که ترجمه‌های خودکار ممکن است حاوی خطاها یا نواقصی باشند. سند اصلی به زبان بومی خود باید به عنوان منبع معتبر در نظر گرفته شود. برای اطلاعات حیاتی، ترجمه حرفه‌ای انسانی توصیه می‌شود. ما مسئول هیچ گونه سوءتفاهم یا تفسیر نادرستی که از استفاده این ترجمه ناشی شود، نیستیم.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->