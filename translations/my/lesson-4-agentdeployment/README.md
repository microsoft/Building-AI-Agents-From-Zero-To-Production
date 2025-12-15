<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:18:17+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "my"
}
-->
# သင်ခန်းစာ ၄: Azure AI Foundry Hosted Agents + ChatKit ဖြင့် Agent တပ်ဆင်ခြင်း

ဤသင်ခန်းစာသည် multi-agent workflow ကို Azure AI Foundry တွင် hosted agent အဖြစ် တပ်ဆင်ပြီး ChatKit အခြေပြု frontend တစ်ခုကို ဖန်တီးကာ အပြန်အလှန် ဆက်သွယ်နိုင်ရန် ပြသသည်။

## အင်ဂျင်နီယာ

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

## မလိုအပ်သောအချက်များ

1. **North Central US ဒေသရှိ Azure AI Foundry Project**
2. **Azure CLI** မှာ အတည်ပြုထားပြီး (`az login`)
3. **Azure Developer CLI** (`azd`) ထည့်သွင်းထားခြင်း
4. **Python 3.12+** နှင့် **Node.js 18+**
5. **ဝန်ထမ်းဒေတာဖြင့် ဖန်တီးထားသော Vector Store**

## အမြန်စတင်ခြင်း

### ၁။ ပတ်ဝန်းကျင်အပြောင်းအလဲများ သတ်မှတ်ခြင်း

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# သင့် Azure AI Foundry ပရောဂျက်အသေးစိတ်များဖြင့် .env ကိုတည်းဖြတ်ပါ
```

### ၂။ Hosted Agent ကို တပ်ဆင်ခြင်း

**ရွေးချယ်စရာ A: Azure Developer CLI အသုံးပြုခြင်း (အကြံပြုသည်)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**ရွေးချယ်စရာ B: Docker + Azure Container Registry အသုံးပြုခြင်း**

```bash
cd hosted-agent

# ကွန်တိန်နာကို တည်ဆောက်ပါ
docker build -t developer-onboarding-agent:latest .

# ACR အတွက် တံဆိပ်တပ်ခြင်း
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR သို့ တင်ပို့ခြင်း
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry ပေါ်တယ် သို့မဟုတ် SDK မှတဆင့် တပ်ဆင်ပါ
```

### ၃။ ChatKit Backend ကို စတင်ပါ

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows တွင်: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

ဆာဗာသည် `http://localhost:8001` တွင် စတင်ပါမည်။

### ၄။ ChatKit Frontend ကို စတင်ပါ

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend သည် `http://localhost:3000` တွင် စတင်ပါမည်။

### ၅။ အပလီကေးရှင်းကို စမ်းသပ်ပါ

သင့်ဘရောက်ဇာတွင် `http://localhost:3000` ကို ဖွင့်ပြီး အောက်ပါမေးခွန်းများကို စမ်းသပ်ကြည့်ပါ။

**ဝန်ထမ်းရှာဖွေရေး:**
- "ကျွန်တော်/ကျွန်မ ဒီမှာအသစ်ပါ! Microsoft မှာ အလုပ်လုပ်ဖူးသူ ရှိပါသလား?"
- "Azure Functions နဲ့ အတွေ့အကြုံရှိသူ ဘယ်သူလဲ?"

**သင်ယူမှု အရင်းအမြစ်များ:**
- "Kubernetes အတွက် သင်ယူမှုလမ်းကြောင်း တစ်ခု ဖန်တီးပါ"
- "Cloud architecture အတွက် ဘယ်လို အသိအမှတ်ပြုလက်မှတ်တွေ ရယူသင့်သလဲ?"

**ကုဒ်ရေးရာ အကူအညီ:**
- "CosmosDB နဲ့ ချိတ်ဆက်ဖို့ Python ကုဒ်ရေးရာ အကူအညီ ပေးပါ"
- "Azure Function တစ်ခု ဖန်တီးနည်း ပြပါ"

**Multi-Agent မေးခွန်းများ:**
- "ကျွန်တော်/ကျွန်မ cloud engineer အဖြစ် စတင်တော့မယ်။ ဘယ်သူနဲ့ ဆက်သွယ်ပြီး ဘာတွေ သင်ယူသင့်သလဲ?"

## ပရောဂျက် ဖွဲ့စည်းမှု

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

## Multi-Agent Workflow

Hosted agent သည် **HandoffBuilder** ကို အသုံးပြုကာ အထူးပြုထားသော agent လေးဦးကို စီမံခန့်ခွဲသည်။

| Agent | အခန်းကဏ္ဍ | ကိရိယာများ |
|-------|------------|-------------|
| **Triage Agent** | ဦးဆောင်သူ - မေးခွန်းများကို အထူးပြုသူများဆီ ပို့ဆောင်သည် | မရှိပါ |
| **Employee Search Agent** | အလုပ်သမားများနှင့် အဖွဲ့ဝင်များ ရှာဖွေသည် | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | သင်ယူမှုလမ်းကြောင်းများနှင့် အကြံပြုချက်များ ဖန်တီးသည် | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | ကုဒ်နမူနာများနှင့် လမ်းညွှန်ချက်များ ထုတ်ပေးသည် | မရှိပါ |

Workflow သည် အောက်ပါအတိုင်း ခွင့်ပြုသည်။
- Triage → မည်သည့် အထူးပြုသူမဆို
- အထူးပြုသူများ → အခြား အထူးပြုသူများ (ဆက်စပ်မေးခွန်းများအတွက်)
- အထူးပြုသူများ → Triage (ခေါင်းစဉ်အသစ်များအတွက်)

## ပြဿနာဖြေရှင်းခြင်း

### Agent မတုံ့ပြန်ခြင်း
- Hosted agent သည် Azure AI Foundry တွင် တပ်ဆင်ပြီး လည်ပတ်နေသည်ကို စစ်ဆေးပါ
- `HOSTED_AGENT_NAME` နှင့် `HOSTED_AGENT_VERSION` သည် သင့်တပ်ဆင်မှုနှင့် ကိုက်ညီမှုရှိသည်ကို စစ်ဆေးပါ

### Vector store အမှားများ
- `VECTOR_STORE_ID` သတ်မှတ်မှုမှန်ကန်မှုကို သေချာစစ်ဆေးပါ
- Vector store တွင် ဝန်ထမ်းဒေတာ ပါဝင်မှုကို အတည်ပြုပါ

### အတည်ပြုမှု အမှားများ
- `az login` ကို ပြန်လည်ဆောင်ရွက်ပါ
- Azure AI Foundry project သို့ ဝင်ရောက်ခွင့် ရှိမှုကို သေချာစစ်ဆေးပါ

## အရင်းအမြစ်များ

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**အကြောင်းကြားချက်**  
ဤစာတမ်းကို AI ဘာသာပြန်ဝန်ဆောင်မှု [Co-op Translator](https://github.com/Azure/co-op-translator) ဖြင့် ဘာသာပြန်ထားပါသည်။ ကျွန်ုပ်တို့သည် တိကျမှန်ကန်မှုအတွက် ကြိုးစားနေသော်လည်း အလိုအလျောက် ဘာသာပြန်ခြင်းတွင် အမှားများ သို့မဟုတ် မှားယွင်းချက်များ ပါဝင်နိုင်ကြောင်း သတိပြုပါရန် မေတ္တာရပ်ခံအပ်ပါသည်။ မူရင်းစာတမ်းကို မိမိဘာသာစကားဖြင့်သာ တရားဝင်အရင်းအမြစ်အဖြစ် သတ်မှတ်စဉ်းစားသင့်ပါသည်။ အရေးကြီးသော အချက်အလက်များအတွက် လူ့ဘာသာပြန်ပညာရှင်မှ ဘာသာပြန်ခြင်းကို အကြံပြုပါသည်။ ဤဘာသာပြန်ချက်ကို အသုံးပြုရာမှ ဖြစ်ပေါ်လာနိုင်သည့် နားလည်မှုမှားယွင်းမှုများ သို့မဟုတ် မှားဖတ်ရှုမှုများအတွက် ကျွန်ုပ်တို့သည် တာဝန်မယူပါ။
<!-- CO-OP TRANSLATOR DISCLAIMER END -->