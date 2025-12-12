<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:59:45+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ne"
}
-->
# पाठ ४: Azure AI Foundry होस्ट गरिएको एजेन्टहरू + ChatKit सँग एजेन्ट परिनियोजन

यस पाठले कसरी बहु-एजेन्ट कार्यप्रवाहलाई Azure AI Foundry मा होस्ट गरिएको एजेन्टको रूपमा परिनियोजन गर्ने र यससँग अन्तरक्रिया गर्न ChatKit-आधारित फ्रन्टएन्ड सिर्जना गर्ने देखाउँछ।

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

## पूर्वआवश्यकताहरू

१. **Azure AI Foundry परियोजना** उत्तर मध्य US क्षेत्र मा
२. **Azure CLI** प्रमाणित (`az login`)
३. **Azure Developer CLI** (`azd`) स्थापना गरिएको
४. **Python 3.12+** र **Node.js 18+**
५. **कर्मचारी डाटासँग Vector Store** सिर्जना गरिएको

## छिटो सुरु

### १. वातावरण चरहरू सेटअप गर्नुहोस्

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# तपाईंको Azure AI Foundry परियोजना विवरणहरूसँग .env सम्पादन गर्नुहोस्
```

### २. होस्ट गरिएको एजेन्ट परिनियोजन गर्नुहोस्

**विकल्प A: Azure Developer CLI प्रयोग गर्दै (सिफारिस गरिएको)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**विकल्प B: Docker + Azure Container Registry प्रयोग गर्दै**

```bash
cd hosted-agent

# कन्टेनर निर्माण गर्नुहोस्
docker build -t developer-onboarding-agent:latest .

# ACR को लागि ट्याग
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR मा पुश गर्नुहोस्
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry पोर्टल वा SDK मार्फत डिप्लोय गर्नुहोस्
```

### ३. ChatKit ब्याकएन्ड सुरु गर्नुहोस्

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # विन्डोजमा: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

सर्भर `http://localhost:8001` मा सुरु हुनेछ

### ४. ChatKit फ्रन्टएन्ड सुरु गर्नुहोस्

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

फ्रन्टएन्ड `http://localhost:3000` मा सुरु हुनेछ

### ५. अनुप्रयोग परीक्षण गर्नुहोस्

`http://localhost:3000` तपाईंको ब्राउजरमा खोल्नुहोस् र यी प्रश्नहरू प्रयास गर्नुहोस्:

**कर्मचारी खोज:**
- "म यहाँ नयाँ हुँ! के कसैले Microsoft मा काम गरेको छ?"
- "कसलाई Azure Functions को अनुभव छ?"

**शिक्षण स्रोतहरू:**
- "Kubernetes को लागि सिकाइ मार्ग सिर्जना गर्नुहोस्"
- "क्लाउड आर्किटेक्चरका लागि कुन प्रमाणपत्रहरू लिनु पर्छ?"

**कोडिङ सहायता:**
- "CosmosDB सँग जडान गर्न Python कोड लेख्न मद्दत गर्नुहोस्"
- "Azure Function कसरी सिर्जना गर्ने देखाउनुहोस्"

**बहु-एजेन्ट प्रश्नहरू:**
- "म क्लाउड इन्जिनियरको रूपमा सुरु गर्दैछु। म कससँग जडान हुनुपर्छ र के सिक्नुपर्छ?"

## परियोजना संरचना

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

## बहु-एजेन्ट कार्यप्रवाह

होस्ट गरिएको एजेन्टले **HandoffBuilder** प्रयोग गरेर चार विशेषज्ञ एजेन्टहरूलाई समन्वय गर्दछ:

| एजेन्ट | भूमिका | उपकरणहरू |
|-------|---------|----------|
| **Triage Agent** | समन्वयक - प्रश्नहरू विशेषज्ञहरूमा पठाउँछ | कुनै छैन |
| **Employee Search Agent** | सहकर्मी र टोली सदस्यहरू खोज्छ | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | सिकाइ मार्गहरू र सिफारिसहरू सिर्जना गर्छ | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | कोड नमूना र मार्गदर्शन उत्पादन गर्छ | कुनै छैन |

कार्यप्रवाहले अनुमति दिन्छ:
- Triage → कुनै पनि विशेषज्ञ
- विशेषज्ञहरू → अन्य विशेषज्ञहरू (सम्बन्धित प्रश्नहरूको लागि)
- विशेषज्ञहरू → Triage (नयाँ विषयहरूको लागि)

## समस्या समाधान

### एजेन्ट प्रतिक्रिया दिँदैन
- होस्ट गरिएको एजेन्ट Azure AI Foundry मा परिनियोजन र चलिरहेको छ कि छैन जाँच गर्नुहोस्
- `HOSTED_AGENT_NAME` र `HOSTED_AGENT_VERSION` तपाईंको परिनियोजनसँग मेल खान्छ कि छैन जाँच गर्नुहोस्

### Vector store त्रुटिहरू
- `VECTOR_STORE_ID` सही सेट गरिएको छ कि छैन सुनिश्चित गर्नुहोस्
- भेक्टर स्टोरमा कर्मचारी डाटा छ कि छैन जाँच गर्नुहोस्

### प्रमाणीकरण त्रुटिहरू
- प्रमाणपत्रहरू ताजा गर्न `az login` चलाउनुहोस्
- तपाईंलाई Azure AI Foundry परियोजनामा पहुँच छ कि छैन सुनिश्चित गर्नुहोस्

## स्रोतहरू

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
यो दस्तावेज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) प्रयोग गरी अनुवाद गरिएको हो। हामी शुद्धताका लागि प्रयासरत छौं, तर कृपया ध्यान दिनुहोस् कि स्वचालित अनुवादमा त्रुटि वा अशुद्धता हुन सक्छ। मूल दस्तावेज यसको मूल भाषामा आधिकारिक स्रोत मानिनु पर्छ। महत्वपूर्ण जानकारीका लागि व्यावसायिक मानव अनुवाद सिफारिस गरिन्छ। यस अनुवादको प्रयोगबाट उत्पन्न कुनै पनि गलतफहमी वा गलत व्याख्याका लागि हामी जिम्मेवार छैनौं।
<!-- CO-OP TRANSLATOR DISCLAIMER END -->