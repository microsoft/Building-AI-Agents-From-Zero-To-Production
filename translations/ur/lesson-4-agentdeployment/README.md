<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:53:06+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ur"
}
-->
# سبق 4: Azure AI Foundry ہوسٹڈ ایجنٹس + ChatKit کے ساتھ ایجنٹ کی تعیناتی

یہ سبق دکھاتا ہے کہ کس طرح ایک کثیر ایجنٹ ورک فلو کو Azure AI Foundry میں بطور ہوسٹڈ ایجنٹ تعینات کیا جائے اور اس کے ساتھ بات چیت کے لیے ChatKit پر مبنی فرنٹ اینڈ بنایا جائے۔

## فن تعمیر

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

## پیشگی ضروریات

1. **Azure AI Foundry پروجیکٹ** شمال وسطی امریکہ کے خطے میں
2. **Azure CLI** مستند شدہ (`az login`)
3. **Azure Developer CLI** (`azd`) انسٹال شدہ
4. **Python 3.12+** اور **Node.js 18+**
5. **ملازمین کے ڈیٹا کے ساتھ ویکٹر اسٹور** تخلیق کیا گیا

## فوری آغاز

### 1. ماحول کے متغیرات سیٹ کریں

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# اپنے Azure AI Foundry پروجیکٹ کی تفصیلات کے ساتھ .env کو ترمیم کریں
```

### 2. ہوسٹڈ ایجنٹ تعینات کریں

**اختیار A: Azure Developer CLI استعمال کرتے ہوئے (تجویز کردہ)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**اختیار B: Docker + Azure Container Registry استعمال کرتے ہوئے**

```bash
cd hosted-agent

# کنٹینر بنائیں
docker build -t developer-onboarding-agent:latest .

# ACR کے لیے ٹیگ
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR پر دھکیلیں
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry پورٹل یا SDK کے ذریعے تعینات کریں
```

### 3. ChatKit بیک اینڈ شروع کریں

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # ونڈوز پر: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

سرور `http://localhost:8001` پر شروع ہوگا

### 4. ChatKit فرنٹ اینڈ شروع کریں

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

فرنٹ اینڈ `http://localhost:3000` پر شروع ہوگا

### 5. ایپلیکیشن کی جانچ کریں

اپنے براؤزر میں `http://localhost:3000` کھولیں اور یہ سوالات آزمائیں:

**ملازمین کی تلاش:**
- "میں یہاں نیا ہوں! کیا کسی نے مائیکروسافٹ میں کام کیا ہے؟"
- "کون Azure Functions کے ساتھ تجربہ رکھتا ہے؟"

**تعلیمی وسائل:**
- "Kubernetes کے لیے ایک تعلیمی راستہ بنائیں"
- "کلاؤڈ آرکیٹیکچر کے لیے کون سی سرٹیفیکیشنز حاصل کرنی چاہئیں؟"

**کوڈنگ مدد:**
- "مجھے CosmosDB سے کنیکٹ کرنے کے لیے Python کوڈ لکھنے میں مدد کریں"
- "مجھے دکھائیں کہ Azure Function کیسے بنائیں"

**کثیر ایجنٹ سوالات:**
- "میں کلاؤڈ انجینئر کے طور پر شروع کر رہا ہوں۔ مجھے کس سے رابطہ کرنا چاہیے اور کیا سیکھنا چاہیے؟"

## پروجیکٹ کا ڈھانچہ

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

## کثیر ایجنٹ ورک فلو

ہوسٹڈ ایجنٹ **HandoffBuilder** استعمال کرتا ہے تاکہ چار مخصوص ایجنٹس کو مربوط کیا جا سکے:

| ایجنٹ | کردار | اوزار |
|-------|-------|-------|
| **Triage Agent** | کوآرڈینیٹر - سوالات کو ماہرین تک پہنچاتا ہے | کوئی نہیں |
| **Employee Search Agent** | ساتھیوں اور ٹیم کے ارکان کو تلاش کرتا ہے | HostedFileSearchTool (ویکٹر اسٹور) |
| **Learning Agent** | تعلیمی راستے اور سفارشات بناتا ہے | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | کوڈ کے نمونے اور رہنمائی فراہم کرتا ہے | کوئی نہیں |

ورک فلو کی اجازت دیتا ہے:
- Triage → کوئی بھی ماہر
- ماہرین → دوسرے ماہرین (متعلقہ سوالات کے لیے)
- ماہرین → Triage (نئے موضوعات کے لیے)

## مسائل کا حل

### ایجنٹ جواب نہیں دے رہا
- تصدیق کریں کہ ہوسٹڈ ایجنٹ Azure AI Foundry میں تعینات اور چل رہا ہے
- چیک کریں کہ `HOSTED_AGENT_NAME` اور `HOSTED_AGENT_VERSION` آپ کی تعیناتی سے میل کھاتے ہیں

### ویکٹر اسٹور کی غلطیاں
- یقینی بنائیں کہ `VECTOR_STORE_ID` درست طریقے سے سیٹ ہے
- تصدیق کریں کہ ویکٹر اسٹور میں ملازمین کا ڈیٹا موجود ہے

### توثیقی غلطیاں
- `az login` چلائیں تاکہ اسناد تازہ ہوں
- یقینی بنائیں کہ آپ کو Azure AI Foundry پروجیکٹ تک رسائی حاصل ہے

## وسائل

- [Azure AI Foundry ہوسٹڈ ایجنٹس کی دستاویزات](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit انٹیگریشن سیمپل](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**دستخطی دستبرداری**:  
یہ دستاویز AI ترجمہ سروس [Co-op Translator](https://github.com/Azure/co-op-translator) کے ذریعے ترجمہ کی گئی ہے۔ اگرچہ ہم درستگی کے لیے کوشاں ہیں، براہ کرم آگاہ رہیں کہ خودکار ترجمے میں غلطیاں یا عدم درستیاں ہو سکتی ہیں۔ اصل دستاویز اپنی مادری زبان میں معتبر ماخذ سمجھی جانی چاہیے۔ اہم معلومات کے لیے پیشہ ور انسانی ترجمہ کی سفارش کی جاتی ہے۔ اس ترجمے کے استعمال سے پیدا ہونے والی کسی بھی غلط فہمی یا غلط تشریح کی ذمہ داری ہم پر عائد نہیں ہوتی۔
<!-- CO-OP TRANSLATOR DISCLAIMER END -->