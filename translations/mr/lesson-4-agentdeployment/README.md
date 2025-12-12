<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:59:01+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "mr"
}
-->
# धडा 4: Azure AI Foundry होस्टेड एजंट्स + ChatKit सह एजंट तैनाती

हा धडा Azure AI Foundry मध्ये होस्टेड एजंट म्हणून मल्टी-एजंट वर्कफ्लो कसे तैनात करायचे आणि त्याच्याशी संवाद साधण्यासाठी ChatKit-आधारित फ्रंटेंड कसे तयार करायचे हे दर्शवितो.

## आर्किटेक्चर

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

## पूर्वअट

1. **Azure AI Foundry प्रोजेक्ट** नॉर्थ सेंट्रल यूएस प्रदेशात
2. **Azure CLI** प्रमाणित (`az login`)
3. **Azure Developer CLI** (`azd`) स्थापित
4. **Python 3.12+** आणि **Node.js 18+**
5. **कर्मचारी डेटासह व्हेक्टर स्टोअर** तयार केलेले

## जलद प्रारंभ

### 1. पर्यावरण चल सेट करा

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# आपल्या Azure AI Foundry प्रकल्प तपशीलांसह .env संपादित करा
```

### 2. होस्टेड एजंट तैनात करा

**पर्याय A: Azure Developer CLI वापरून (शिफारस केलेले)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**पर्याय B: Docker + Azure Container Registry वापरून**

```bash
cd hosted-agent

# कंटेनर तयार करा
docker build -t developer-onboarding-agent:latest .

# ACR साठी टॅग
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR मध्ये ढकलणे
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry पोर्टल किंवा SDK द्वारे तैनात करा
```

### 3. ChatKit बॅकएंड सुरू करा

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows वर: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

सर्व्हर `http://localhost:8001` वर सुरू होईल

### 4. ChatKit फ्रंटएंड सुरू करा

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

फ्रंटएंड `http://localhost:3000` वर सुरू होईल

### 5. अनुप्रयोगाची चाचणी करा

`http://localhost:3000` तुमच्या ब्राउझरमध्ये उघडा आणि हे प्रश्न विचारून पहा:

**कर्मचारी शोध:**
- "मी नवीन आहे! Microsoft मध्ये कोण काम केले आहे का?"
- "Azure Functions मध्ये कोणाला अनुभव आहे?"

**शिकण्याचे स्रोत:**
- "Kubernetes साठी शिकण्याचा मार्ग तयार करा"
- "क्लाउड आर्किटेक्चरसाठी कोणती प्रमाणपत्रे घ्यावी?"

**कोडिंग मदत:**
- "CosmosDB शी कनेक्ट होण्यासाठी Python कोड लिहायला मदत करा"
- "Azure Function कसे तयार करायचे ते दाखवा"

**मल्टी-एजंट प्रश्न:**
- "मी क्लाउड इंजिनियर म्हणून सुरुवात करत आहे. मला कोणाशी संपर्क साधावा आणि काय शिकावे?"

## प्रोजेक्ट रचना

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

## मल्टी-एजंट वर्कफ्लो

होस्टेड एजंट **HandoffBuilder** वापरून चार विशेष एजंट्सचे समन्वय साधतो:

| एजंट | भूमिका | साधने |
|-------|---------|--------|
| **Triage Agent** | समन्वयक - प्रश्न तज्ञांकडे मार्गदर्शन करतो | नाही |
| **Employee Search Agent** | सहकारी आणि टीम सदस्य शोधतो | HostedFileSearchTool (व्हेक्टर स्टोअर) |
| **Learning Agent** | शिकण्याचे मार्ग आणि शिफारसी तयार करतो | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | कोड नमुने आणि मार्गदर्शन तयार करतो | नाही |

वर्कफ्लो परवानगी देतो:
- Triage → कोणताही तज्ञ
- तज्ञ → इतर तज्ञ (संबंधित प्रश्नांसाठी)
- तज्ञ → Triage (नवीन विषयांसाठी)

## समस्या निवारण

### एजंट प्रतिसाद देत नाही
- होस्टेड एजंट Azure AI Foundry मध्ये तैनात आणि चालू आहे का तपासा
- `HOSTED_AGENT_NAME` आणि `HOSTED_AGENT_VERSION` तुमच्या तैनातीशी जुळतात का तपासा

### व्हेक्टर स्टोअर त्रुटी
- `VECTOR_STORE_ID` योग्यरित्या सेट आहे का तपासा
- व्हेक्टर स्टोअरमध्ये कर्मचारी डेटा आहे का तपासा

### प्रमाणीकरण त्रुटी
- `az login` चालवा आणि क्रेडेन्शियल्स ताजेतवाने करा
- Azure AI Foundry प्रोजेक्टमध्ये तुमची प्रवेश परवानगी आहे का तपासा

## संसाधने

- [Azure AI Foundry Hosted Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**अस्वीकरण**:
हा दस्तऐवज AI अनुवाद सेवा [Co-op Translator](https://github.com/Azure/co-op-translator) वापरून अनुवादित केला आहे. आम्ही अचूकतेसाठी प्रयत्नशील असलो तरी, कृपया लक्षात घ्या की स्वयंचलित अनुवादांमध्ये चुका किंवा अचूकतेची कमतरता असू शकते. मूळ दस्तऐवज त्याच्या स्थानिक भाषेत अधिकृत स्रोत मानला जावा. महत्त्वाच्या माहितीसाठी व्यावसायिक मानवी अनुवाद शिफारसीय आहे. या अनुवादाच्या वापरामुळे उद्भवणाऱ्या कोणत्याही गैरसमजुती किंवा चुकीच्या अर्थलागी आम्ही जबाबदार नाही.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->