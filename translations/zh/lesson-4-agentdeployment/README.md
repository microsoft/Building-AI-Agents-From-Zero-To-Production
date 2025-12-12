<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:53:41+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "zh"
}
-->
# Lesson 4: 使用 Azure AI Foundry 托管代理 + ChatKit 部署代理

本课演示如何将多代理工作流部署到 Azure AI Foundry 作为托管代理，并创建基于 ChatKit 的前端与其交互。

## 架构

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

## 前提条件

1. 位于北中美洲地区的 **Azure AI Foundry 项目**
2. 已认证的 **Azure CLI**（`az login`）
3. 已安装 **Azure Developer CLI**（`azd`）
4. **Python 3.12+** 和 **Node.js 18+**
5. 使用员工数据创建的 **向量存储**

## 快速开始

### 1. 设置环境变量

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# 使用您的 Azure AI Foundry 项目详细信息编辑 .env
```

### 2. 部署托管代理

**选项 A：使用 Azure Developer CLI（推荐）**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**选项 B：使用 Docker + Azure 容器注册表**

```bash
cd hosted-agent

# 构建容器
docker build -t developer-onboarding-agent:latest .

# ACR 的标签
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# 推送到 ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# 通过 Azure AI Foundry 门户或 SDK 部署
```

### 3. 启动 ChatKit 后端

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # 在 Windows 上：.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

服务器将在 `http://localhost:8001` 启动

### 4. 启动 ChatKit 前端

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

前端将在 `http://localhost:3000` 启动

### 5. 测试应用

在浏览器中打开 `http://localhost:3000` 并尝试以下查询：

**员工搜索：**
- “我刚来这里！有人在微软工作过吗？”
- “谁有 Azure Functions 的经验？”

**学习资源：**
- “为 Kubernetes 创建学习路径”
- “我应该考哪些认证来成为云架构师？”

**编码帮助：**
- “帮我写连接 CosmosDB 的 Python 代码”
- “告诉我如何创建 Azure Function”

**多代理查询：**
- “我刚开始做云工程师。应该联系谁，学习什么？”

## 项目结构

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

## 多代理工作流

托管代理使用 **HandoffBuilder** 来协调四个专门代理：

| 代理 | 角色 | 工具 |
|-------|------|-------|
| **分诊代理** | 协调者 - 将查询路由给专家 | 无 |
| **员工搜索代理** | 查找同事和团队成员 | HostedFileSearchTool（向量存储） |
| **学习代理** | 创建学习路径和推荐 | HostedMCPTool（Microsoft Learn） |
| **编码代理** | 生成代码示例和指导 | 无 |

工作流允许：
- 分诊 → 任意专家
- 专家 → 其他专家（处理相关查询）
- 专家 → 分诊（处理新主题）

## 故障排除

### 代理无响应
- 确认托管代理已部署并在 Azure AI Foundry 运行
- 检查 `HOSTED_AGENT_NAME` 和 `HOSTED_AGENT_VERSION` 是否与部署匹配

### 向量存储错误
- 确保正确设置了 `VECTOR_STORE_ID`
- 验证向量存储包含员工数据

### 认证错误
- 运行 `az login` 刷新凭据
- 确保你有访问 Azure AI Foundry 项目的权限

## 资源

- [Azure AI Foundry 托管代理文档](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft 代理框架](https://github.com/microsoft/agent-framework)
- [ChatKit 集成示例](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：  
本文件由人工智能翻译服务 [Co-op Translator](https://github.com/Azure/co-op-translator) 翻译而成。虽然我们力求准确，但请注意自动翻译可能存在错误或不准确之处。原始文件的母语版本应被视为权威来源。对于重要信息，建议使用专业人工翻译。因使用本翻译而产生的任何误解或误释，我们概不负责。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->