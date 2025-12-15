<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:57:29+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "hi"
}
-->
# पाठ 4: Azure AI Foundry होस्टेड एजेंट्स + ChatKit के साथ एजेंट तैनाती

यह पाठ दिखाता है कि कैसे एक मल्टी-एजेंट वर्कफ़्लो को Azure AI Foundry में एक होस्टेड एजेंट के रूप में तैनात किया जाए और इसके साथ बातचीत करने के लिए ChatKit-आधारित फ्रंटेंड बनाया जाए।

## वास्तुकला

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

## पूर्वापेक्षाएँ

1. **Azure AI Foundry प्रोजेक्ट** नॉर्थ सेंट्रल यूएस क्षेत्र में
2. **Azure CLI** प्रमाणीकृत (`az login`)
3. **Azure Developer CLI** (`azd`) इंस्टॉल किया हुआ
4. **Python 3.12+** और **Node.js 18+**
5. **कर्मचारी डेटा के साथ वेक्टर स्टोर** बनाया हुआ

## त्वरित प्रारंभ

### 1. पर्यावरण चर सेट करें

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# अपने Azure AI Foundry प्रोजेक्ट विवरण के साथ .env संपादित करें
```

### 2. होस्टेड एजेंट तैनात करें

**विकल्प A: Azure Developer CLI का उपयोग करना (अनुशंसित)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**विकल्प B: Docker + Azure Container Registry का उपयोग करना**

```bash
cd hosted-agent

# कंटेनर बनाएं
docker build -t developer-onboarding-agent:latest .

# ACR के लिए टैग
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR में पुश करें
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry पोर्टल या SDK के माध्यम से तैनात करें
```

### 3. ChatKit बैकएंड शुरू करें

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # विंडोज़ पर: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

सर्वर `http://localhost:8001` पर शुरू होगा

### 4. ChatKit फ्रंटेंड शुरू करें

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

फ्रंटेंड `http://localhost:3000` पर शुरू होगा

### 5. एप्लिकेशन का परीक्षण करें

अपने ब्राउज़र में `http://localhost:3000` खोलें और ये प्रश्न आज़माएं:

**कर्मचारी खोज:**
- "मैं यहाँ नया हूँ! क्या किसी ने Microsoft में काम किया है?"
- "किसके पास Azure Functions का अनुभव है?"

**शिक्षण संसाधन:**
- "Kubernetes के लिए एक लर्निंग पाथ बनाएं"
- "क्लाउड आर्किटेक्चर के लिए मुझे कौन-से प्रमाणपत्र लेने चाहिए?"

**कोडिंग सहायता:**
- "मुझे CosmosDB से कनेक्ट करने के लिए Python कोड लिखने में मदद करें"
- "मुझे दिखाएं कि Azure Function कैसे बनाएं"

**मल्टी-एजेंट प्रश्न:**
- "मैं क्लाउड इंजीनियर के रूप में शुरू कर रहा हूँ। मुझे किससे जुड़ना चाहिए और क्या सीखना चाहिए?"

## प्रोजेक्ट संरचना

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

## मल्टी-एजेंट वर्कफ़्लो

होस्टेड एजेंट **HandoffBuilder** का उपयोग करके चार विशेषज्ञ एजेंटों का समन्वय करता है:

| एजेंट | भूमिका | उपकरण |
|-------|---------|--------|
| **ट्रायज एजेंट** | समन्वयक - प्रश्नों को विशेषज्ञों तक पहुँचाता है | कोई नहीं |
| **कर्मचारी खोज एजेंट** | सहकर्मियों और टीम सदस्यों को खोजता है | HostedFileSearchTool (वेक्टर स्टोर) |
| **शिक्षण एजेंट** | लर्निंग पाथ और सिफारिशें बनाता है | HostedMCPTool (Microsoft Learn) |
| **कोडिंग एजेंट** | कोड नमूने और मार्गदर्शन उत्पन्न करता है | कोई नहीं |

वर्कफ़्लो अनुमति देता है:
- ट्रायज → कोई भी विशेषज्ञ
- विशेषज्ञ → अन्य विशेषज्ञ (संबंधित प्रश्नों के लिए)
- विशेषज्ञ → ट्रायज (नए विषयों के लिए)

## समस्या निवारण

### एजेंट प्रतिक्रिया नहीं दे रहा
- सुनिश्चित करें कि होस्टेड एजेंट Azure AI Foundry में तैनात और चल रहा है
- जांचें कि `HOSTED_AGENT_NAME` और `HOSTED_AGENT_VERSION` आपकी तैनाती से मेल खाते हैं

### वेक्टर स्टोर त्रुटियाँ
- सुनिश्चित करें कि `VECTOR_STORE_ID` सही सेट है
- वेक्टर स्टोर में कर्मचारी डेटा मौजूद है यह सत्यापित करें

### प्रमाणीकरण त्रुटियाँ
- क्रेडेंशियल्स को ताज़ा करने के लिए `az login` चलाएं
- सुनिश्चित करें कि आपके पास Azure AI Foundry प्रोजेक्ट तक पहुँच है

## संसाधन

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:  
इस दस्तावेज़ का अनुवाद AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) का उपयोग करके किया गया है। जबकि हम सटीकता के लिए प्रयासरत हैं, कृपया ध्यान दें कि स्वचालित अनुवाद में त्रुटियाँ या अशुद्धियाँ हो सकती हैं। मूल दस्तावेज़ अपनी मूल भाषा में ही प्रामाणिक स्रोत माना जाना चाहिए। महत्वपूर्ण जानकारी के लिए, पेशेवर मानव अनुवाद की सलाह दी जाती है। इस अनुवाद के उपयोग से उत्पन्न किसी भी गलतफहमी या गलत व्याख्या के लिए हम जिम्मेदार नहीं हैं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->