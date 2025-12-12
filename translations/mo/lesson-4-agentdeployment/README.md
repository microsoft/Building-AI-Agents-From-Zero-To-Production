<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:54:21+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "mo"
}
-->
# Lesson 4: 使用 Azure AI Foundry 託管代理 + ChatKit 進行代理部署

本課程示範如何將多代理工作流程部署到 Azure AI Foundry 作為託管代理，並建立基於 ChatKit 的前端與其互動。

## 架構

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

## 先決條件

1. 位於北中美地區的 **Azure AI Foundry 專案**
2. 已驗證的 **Azure CLI** (`az login`)
3. 已安裝 **Azure Developer CLI** (`azd`)
4. **Python 3.12+** 與 **Node.js 18+**
5. 已建立包含員工資料的 **向量資料庫**

## 快速開始

### 1. 設定環境變數

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# 使用您的 Azure AI Foundry 專案詳情編輯 .env
```

### 2. 部署託管代理

**選項 A：使用 Azure Developer CLI（推薦）**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**選項 B：使用 Docker + Azure Container Registry**

```bash
cd hosted-agent

# 建立容器
docker build -t developer-onboarding-agent:latest .

# ACR 標籤
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# 推送到 ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# 透過 Azure AI Foundry 入口網站或 SDK 部署
```

### 3. 啟動 ChatKit 後端

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # 喺 Windows：.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

伺服器將在 `http://localhost:8001` 啟動

### 4. 啟動 ChatKit 前端

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

前端將在 `http://localhost:3000` 啟動

### 5. 測試應用程式

在瀏覽器開啟 `http://localhost:3000` 並嘗試以下查詢：

**員工搜尋：**
- 「我剛來這裡！有人在 Microsoft 工作過嗎？」
- 「誰有 Azure Functions 的經驗？」

**學習資源：**
- 「建立 Kubernetes 的學習路徑」
- 「我應該追求哪些雲端架構的認證？」

**程式協助：**
- 「幫我寫連接 CosmosDB 的 Python 程式碼」
- 「示範如何建立 Azure Function」

**多代理查詢：**
- 「我剛開始當雲端工程師。應該跟誰聯繫，該學什麼？」

## 專案結構

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

## 多代理工作流程

託管代理使用 **HandoffBuilder** 來協調四個專門代理：

| 代理 | 角色 | 工具 |
|-------|------|-------|
| **分流代理** | 協調者 - 將查詢導向專家 | 無 |
| **員工搜尋代理** | 尋找同事與團隊成員 | HostedFileSearchTool（向量資料庫） |
| **學習代理** | 建立學習路徑與推薦 | HostedMCPTool（Microsoft Learn） |
| **程式代理** | 產生程式範例與指導 | 無 |

工作流程允許：
- 分流 → 任一專家
- 專家 → 其他專家（處理相關查詢）
- 專家 → 分流（處理新主題）

## 疑難排解

### 代理無回應
- 確認託管代理已部署並在 Azure AI Foundry 運行
- 檢查 `HOSTED_AGENT_NAME` 與 `HOSTED_AGENT_VERSION` 是否與部署相符

### 向量資料庫錯誤
- 確認 `VECTOR_STORE_ID` 設定正確
- 驗證向量資料庫包含員工資料

### 認證錯誤
- 執行 `az login` 以更新憑證
- 確認您有權限存取 Azure AI Foundry 專案

## 資源

- [Azure AI Foundry 託管代理文件](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit 整合範例](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件之母語版本應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起之任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->