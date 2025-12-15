<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:51:50+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ar"
}
-->
# الدرس 4: نشر الوكيل مع وكلاء Azure AI Foundry المستضافين + ChatKit

يُظهر هذا الدرس كيفية نشر سير عمل متعدد الوكلاء إلى Azure AI Foundry كوكيل مستضاف وإنشاء واجهة أمامية تعتمد على ChatKit للتفاعل معه.

## البنية المعمارية

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

## المتطلبات الأساسية

1. **مشروع Azure AI Foundry** في منطقة شمال وسط الولايات المتحدة
2. **Azure CLI** مصادق عليه (`az login`)
3. **Azure Developer CLI** (`azd`) مثبت
4. **Python 3.12+** و **Node.js 18+**
5. **مخزن متجهات** تم إنشاؤه ببيانات الموظفين

## البدء السريع

### 1. إعداد متغيرات البيئة

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# حرر ملف .env بتفاصيل مشروع Azure AI Foundry الخاص بك
```

### 2. نشر الوكيل المستضاف

**الخيار أ: استخدام Azure Developer CLI (موصى به)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**الخيار ب: استخدام Docker + Azure Container Registry**

```bash
cd hosted-agent

# بناء الحاوية
docker build -t developer-onboarding-agent:latest .

# الوسم لـ ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# الدفع إلى ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# النشر عبر بوابة Azure AI Foundry أو SDK
```

### 3. بدء تشغيل الخلفية الخاصة بـ ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

سيبدأ الخادم على `http://localhost:8001`

### 4. بدء تشغيل الواجهة الأمامية الخاصة بـ ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ستبدأ الواجهة الأمامية على `http://localhost:3000`

### 5. اختبار التطبيق

افتح `http://localhost:3000` في متصفحك وجرب هذه الاستفسارات:

**البحث عن الموظفين:**
- "أنا جديد هنا! هل عمل أحد في مايكروسوفت؟"
- "من لديه خبرة في Azure Functions؟"

**موارد التعلم:**
- "أنشئ مسار تعلم لـ Kubernetes"
- "ما الشهادات التي يجب أن أسعى للحصول عليها لهندسة السحابة؟"

**مساعدة في البرمجة:**
- "ساعدني في كتابة كود بايثون للاتصال بـ CosmosDB"
- "أرني كيف أنشئ Azure Function"

**استفسارات متعددة الوكلاء:**
- "أنا أبدأ كمهندس سحابة. من يجب أن أتواصل معه وماذا يجب أن أتعلم؟"

## هيكل المشروع

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

## سير العمل متعدد الوكلاء

يستخدم الوكيل المستضاف **HandoffBuilder** لتنظيم أربعة وكلاء متخصصين:

| الوكيل | الدور | الأدوات |
|-------|-------|---------|
| **وكيل الفرز** | المنسق - يوجه الاستفسارات إلى المتخصصين | لا شيء |
| **وكيل البحث عن الموظفين** | يعثر على الزملاء وأعضاء الفريق | HostedFileSearchTool (مخزن المتجهات) |
| **وكيل التعلم** | ينشئ مسارات التعلم والتوصيات | HostedMCPTool (Microsoft Learn) |
| **وكيل البرمجة** | يولد عينات كود وإرشادات | لا شيء |

يسمح سير العمل بـ:
- الفرز → أي متخصص
- المتخصصون → متخصصون آخرون (للاستفسارات ذات الصلة)
- المتخصصون → الفرز (للمواضيع الجديدة)

## استكشاف الأخطاء وإصلاحها

### الوكيل لا يستجيب
- تحقق من أن الوكيل المستضاف تم نشره ويعمل في Azure AI Foundry
- تحقق من تطابق `HOSTED_AGENT_NAME` و `HOSTED_AGENT_VERSION` مع نشراتك

### أخطاء مخزن المتجهات
- تأكد من تعيين `VECTOR_STORE_ID` بشكل صحيح
- تحقق من أن مخزن المتجهات يحتوي على بيانات الموظفين

### أخطاء المصادقة
- نفذ `az login` لتحديث بيانات الاعتماد
- تأكد من أن لديك حق الوصول إلى مشروع Azure AI Foundry

## الموارد

- [توثيق وكلاء Azure AI Foundry المستضافين](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [إطار عمل وكلاء مايكروسوفت](https://github.com/microsoft/agent-framework)
- [عينة تكامل ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق به. للمعلومات الهامة، يُنصح بالاعتماد على الترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->