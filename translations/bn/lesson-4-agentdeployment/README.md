<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:58:13+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "bn"
}
-->
# পাঠ ৪: Azure AI Foundry হোস্টেড এজেন্ট + ChatKit সহ এজেন্ট ডিপ্লয়মেন্ট

এই পাঠে দেখানো হয়েছে কিভাবে একটি মাল্টি-এজেন্ট ওয়ার্কফ্লো Azure AI Foundry-তে হোস্টেড এজেন্ট হিসেবে ডিপ্লয় করতে হয় এবং এর সাথে ইন্টারঅ্যাক্ট করার জন্য ChatKit-ভিত্তিক ফ্রন্টএন্ড তৈরি করতে হয়।

## আর্কিটেকচার

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

## পূর্বশর্ত

১. **Azure AI Foundry প্রকল্প** নর্থ সেন্ট্রাল ইউএস অঞ্চলে  
২. **Azure CLI** প্রমাণীকৃত (`az login`)  
৩. **Azure Developer CLI** (`azd`) ইনস্টল করা  
৪. **Python 3.12+** এবং **Node.js 18+**  
৫. **ভেক্টর স্টোর** কর্মচারী ডেটা সহ তৈরি করা হয়েছে  

## দ্রুত শুরু

### ১. পরিবেশ ভেরিয়েবল সেট আপ করুন

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# আপনার Azure AI Foundry প্রকল্পের বিবরণ সহ .env সম্পাদনা করুন
```

### ২. হোস্টেড এজেন্ট ডিপ্লয় করুন

**অপশন এ: Azure Developer CLI ব্যবহার করে (প্রস্তাবিত)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**অপশন বি: Docker + Azure Container Registry ব্যবহার করে**

```bash
cd hosted-agent

# কন্টেইনার তৈরি করুন
docker build -t developer-onboarding-agent:latest .

# ACR এর জন্য ট্যাগ
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR এ পুশ করুন
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry পোর্টাল বা SDK এর মাধ্যমে ডিপ্লয় করুন
```

### ৩. ChatKit ব্যাকএন্ড শুরু করুন

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # উইন্ডোজে: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

সার্ভার শুরু হবে `http://localhost:8001` এ

### ৪. ChatKit ফ্রন্টএন্ড শুরু করুন

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

ফ্রন্টএন্ড শুরু হবে `http://localhost:3000` এ

### ৫. অ্যাপ্লিকেশন পরীক্ষা করুন

আপনার ব্রাউজারে `http://localhost:3000` খুলুন এবং এই প্রশ্নগুলো চেষ্টা করুন:

**কর্মচারী অনুসন্ধান:**  
- "আমি এখানে নতুন! কেউ কি Microsoft-এ কাজ করেছেন?"  
- "কার Azure Functions-এ অভিজ্ঞতা আছে?"

**শিক্ষণ সম্পদ:**  
- "Kubernetes-এর জন্য একটি শেখার পথ তৈরি করুন"  
- "ক্লাউড আর্কিটেকচারের জন্য কোন সার্টিফিকেশনগুলি করা উচিত?"

**কোডিং সাহায্য:**  
- "CosmosDB-তে সংযোগ করার জন্য Python কোড লিখতে সাহায্য করুন"  
- "আমাকে দেখান কিভাবে একটি Azure Function তৈরি করতে হয়"

**মাল্টি-এজেন্ট প্রশ্ন:**  
- "আমি ক্লাউড ইঞ্জিনিয়ার হিসেবে শুরু করছি। কার সাথে সংযোগ করব এবং কি শিখব?"

## প্রকল্পের কাঠামো

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

## মাল্টি-এজেন্ট ওয়ার্কফ্লো

হোস্টেড এজেন্ট **HandoffBuilder** ব্যবহার করে চারটি বিশেষায়িত এজেন্টকে সমন্বয় করে:

| এজেন্ট | ভূমিকা | সরঞ্জামসমূহ |
|--------|---------|-------------|
| **ট্রায়াজ এজেন্ট** | সমন্বয়কারী - প্রশ্নগুলো বিশেষজ্ঞদের কাছে রুট করে | কোনটি নয় |
| **কর্মচারী অনুসন্ধান এজেন্ট** | সহকর্মী ও টিম সদস্য খুঁজে বের করে | HostedFileSearchTool (ভেক্টর স্টোর) |
| **শিক্ষণ এজেন্ট** | শেখার পথ ও সুপারিশ তৈরি করে | HostedMCPTool (Microsoft Learn) |
| **কোডিং এজেন্ট** | কোড নমুনা ও নির্দেশনা তৈরি করে | কোনটি নয় |

ওয়ার্কফ্লো অনুমোদন করে:  
- ট্রায়াজ → যেকোনো বিশেষজ্ঞ  
- বিশেষজ্ঞ → অন্য বিশেষজ্ঞ (সম্পর্কিত প্রশ্নের জন্য)  
- বিশেষজ্ঞ → ট্রায়াজ (নতুন বিষয়ের জন্য)  

## সমস্যা সমাধান

### এজেন্ট সাড়া দিচ্ছে না
- নিশ্চিত করুন হোস্টেড এজেন্ট Azure AI Foundry-তে ডিপ্লয় ও চালু আছে  
- `HOSTED_AGENT_NAME` এবং `HOSTED_AGENT_VERSION` আপনার ডিপ্লয়মেন্টের সাথে মেলে কিনা যাচাই করুন  

### ভেক্টর স্টোর ত্রুটি
- নিশ্চিত করুন `VECTOR_STORE_ID` সঠিকভাবে সেট করা হয়েছে  
- ভেক্টর স্টোরে কর্মচারী ডেটা আছে কিনা যাচাই করুন  

### প্রমাণীকরণ ত্রুটি
- `az login` চালিয়ে শংসাপত্র রিফ্রেশ করুন  
- নিশ্চিত করুন আপনার Azure AI Foundry প্রকল্পে অ্যাক্সেস আছে  

## সম্পদসমূহ

- [Azure AI Foundry হোস্টেড এজেন্ট ডকুমেন্টেশন](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)  
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)  
- [ChatKit ইন্টিগ্রেশন স্যাম্পল](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)  
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**অস্বীকৃতি**:  
এই নথিটি AI অনুবাদ সেবা [Co-op Translator](https://github.com/Azure/co-op-translator) ব্যবহার করে অনূদিত হয়েছে। আমরা যথাসাধ্য সঠিকতার চেষ্টা করি, তবে স্বয়ংক্রিয় অনুবাদে ত্রুটি বা অসঙ্গতি থাকতে পারে। মূল নথিটি তার নিজস্ব ভাষায়ই কর্তৃত্বপূর্ণ উৎস হিসেবে বিবেচিত হওয়া উচিত। গুরুত্বপূর্ণ তথ্যের জন্য পেশাদার মানব অনুবাদ গ্রহণ করার পরামর্শ দেওয়া হয়। এই অনুবাদের ব্যবহারে সৃষ্ট কোনো ভুল বোঝাবুঝি বা ভুল ব্যাখ্যার জন্য আমরা দায়ী নই।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->