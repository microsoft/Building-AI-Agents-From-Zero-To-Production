<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:05:25+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "th"
}
-->
# บทที่ 4: การปรับใช้ Agent ด้วย Azure AI Foundry Hosted Agents + ChatKit

บทเรียนนี้แสดงวิธีการปรับใช้เวิร์กโฟลว์หลายเอเจนต์ไปยัง Azure AI Foundry ในฐานะโฮสต์เอเจนต์และสร้าง frontend บนพื้นฐาน ChatKit เพื่อโต้ตอบกับมัน

## สถาปัตยกรรม

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

## ข้อกำหนดเบื้องต้น

1. **โครงการ Azure AI Foundry** ในภูมิภาค North Central US
2. **Azure CLI** ที่ผ่านการตรวจสอบสิทธิ์ (`az login`)
3. ติดตั้ง **Azure Developer CLI** (`azd`)
4. **Python 3.12+** และ **Node.js 18+**
5. สร้าง **Vector Store** ด้วยข้อมูลพนักงาน

## เริ่มต้นอย่างรวดเร็ว

### 1. ตั้งค่าตัวแปรสภาพแวดล้อม

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# แก้ไข .env ด้วยรายละเอียดโครงการ Azure AI Foundry ของคุณ
```

### 2. ปรับใช้ Hosted Agent

**ตัวเลือก A: ใช้ Azure Developer CLI (แนะนำ)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**ตัวเลือก B: ใช้ Docker + Azure Container Registry**

```bash
cd hosted-agent

# สร้างคอนเทนเนอร์
docker build -t developer-onboarding-agent:latest .

# แท็กสำหรับ ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ดันไปยัง ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ติดตั้งผ่านพอร์ทัล Azure AI Foundry หรือ SDK
```

### 3. เริ่มต้น ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # บน Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

เซิร์ฟเวอร์จะเริ่มต้นที่ `http://localhost:8001`

### 4. เริ่มต้น ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend จะเริ่มต้นที่ `http://localhost:3000`

### 5. ทดสอบแอปพลิเคชัน

เปิด `http://localhost:3000` ในเบราว์เซอร์ของคุณและลองใช้คำถามเหล่านี้:

**ค้นหาพนักงาน:**
- "ฉันเพิ่งเข้ามาใหม่! มีใครเคยทำงานที่ Microsoft ไหม?"
- "ใครมีประสบการณ์กับ Azure Functions บ้าง?"

**แหล่งเรียนรู้:**
- "สร้างเส้นทางการเรียนรู้สำหรับ Kubernetes"
- "ฉันควรได้รับการรับรองอะไรบ้างสำหรับสถาปัตยกรรมคลาวด์?"

**ช่วยเขียนโค้ด:**
- "ช่วยฉันเขียนโค้ด Python สำหรับเชื่อมต่อกับ CosmosDB"
- "แสดงวิธีสร้าง Azure Function ให้ฉัน"

**คำถามหลายเอเจนต์:**
- "ฉันเริ่มต้นเป็นวิศวกรคลาวด์ ควรเชื่อมต่อกับใครและควรเรียนรู้อะไรบ้าง?"

## โครงสร้างโครงการ

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

## เวิร์กโฟลว์หลายเอเจนต์

Hosted agent ใช้ **HandoffBuilder** เพื่อประสานงานเอเจนต์เฉพาะทางสี่ตัว:

| Agent | บทบาท | เครื่องมือ |
|-------|--------|------------|
| **Triage Agent** | ผู้ประสานงาน - ส่งคำถามไปยังผู้เชี่ยวชาญ | ไม่มี |
| **Employee Search Agent** | ค้นหาพนักงานและสมาชิกทีม | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | สร้างเส้นทางการเรียนรู้และคำแนะนำ | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | สร้างตัวอย่างโค้ดและคำแนะนำ | ไม่มี |

เวิร์กโฟลว์อนุญาตให้:
- Triage → ผู้เชี่ยวชาญใดก็ได้
- ผู้เชี่ยวชาญ → ผู้เชี่ยวชาญอื่น (สำหรับคำถามที่เกี่ยวข้อง)
- ผู้เชี่ยวชาญ → Triage (สำหรับหัวข้อใหม่)

## การแก้ไขปัญหา

### เอเจนต์ไม่ตอบสนอง
- ตรวจสอบว่า hosted agent ถูกปรับใช้และกำลังทำงานใน Azure AI Foundry
- ตรวจสอบว่า `HOSTED_AGENT_NAME` และ `HOSTED_AGENT_VERSION` ตรงกับการปรับใช้ของคุณ

### ข้อผิดพลาด Vector store
- ตรวจสอบให้แน่ใจว่า `VECTOR_STORE_ID` ตั้งค่าอย่างถูกต้อง
- ยืนยันว่า vector store มีข้อมูลพนักงาน

### ข้อผิดพลาดการตรวจสอบสิทธิ์
- รัน `az login` เพื่อรีเฟรชข้อมูลรับรอง
- ตรวจสอบว่าคุณมีสิทธิ์เข้าถึงโครงการ Azure AI Foundry

## แหล่งข้อมูล

- [เอกสาร Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ตัวอย่างการผสานรวม ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษาอัตโนมัติ [Co-op Translator](https://github.com/Azure/co-op-translator) แม้ว่าเราจะพยายามให้ความถูกต้องสูงสุด แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลโดยผู้เชี่ยวชาญมนุษย์ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดใด ๆ ที่เกิดจากการใช้การแปลนี้
<!-- CO-OP TRANSLATOR DISCLAIMER END -->