<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:09:43+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "vi"
}
-->
# Bài học 4: Triển khai Agent với Azure AI Foundry Hosted Agents + ChatKit

Bài học này trình bày cách triển khai một quy trình làm việc đa agent lên Azure AI Foundry dưới dạng một hosted agent và tạo một frontend dựa trên ChatKit để tương tác với nó.

## Kiến trúc

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

## Yêu cầu trước

1. **Dự án Azure AI Foundry** trong khu vực North Central US
2. **Azure CLI** đã xác thực (`az login`)
3. **Azure Developer CLI** (`azd`) đã cài đặt
4. **Python 3.12+** và **Node.js 18+**
5. **Vector Store** đã được tạo với dữ liệu nhân viên

## Bắt đầu nhanh

### 1. Thiết lập biến môi trường

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Chỉnh sửa .env với chi tiết dự án Azure AI Foundry của bạn
```

### 2. Triển khai Hosted Agent

**Lựa chọn A: Sử dụng Azure Developer CLI (Khuyến nghị)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Lựa chọn B: Sử dụng Docker + Azure Container Registry**

```bash
cd hosted-agent

# Xây dựng container
docker build -t developer-onboarding-agent:latest .

# Gắn thẻ cho ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Đẩy lên ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Triển khai qua cổng Azure AI Foundry hoặc SDK
```

### 3. Khởi động ChatKit Backend

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Trên Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Máy chủ sẽ khởi động tại `http://localhost:8001`

### 4. Khởi động ChatKit Frontend

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend sẽ khởi động tại `http://localhost:3000`

### 5. Kiểm tra ứng dụng

Mở `http://localhost:3000` trong trình duyệt và thử các truy vấn sau:

**Tìm kiếm nhân viên:**
- "Tôi mới ở đây! Có ai đã làm việc tại Microsoft chưa?"
- "Ai có kinh nghiệm với Azure Functions?"

**Tài nguyên học tập:**
- "Tạo một lộ trình học Kubernetes"
- "Tôi nên theo đuổi những chứng chỉ nào cho kiến trúc đám mây?"

**Hỗ trợ lập trình:**
- "Giúp tôi viết mã Python để kết nối với CosmosDB"
- "Cho tôi xem cách tạo một Azure Function"

**Truy vấn đa agent:**
- "Tôi bắt đầu làm kỹ sư đám mây. Tôi nên kết nối với ai và nên học gì?"

## Cấu trúc dự án

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

## Quy trình làm việc đa agent

Hosted agent sử dụng **HandoffBuilder** để điều phối bốn agent chuyên biệt:

| Agent | Vai trò | Công cụ |
|-------|---------|---------|
| **Triage Agent** | Điều phối - chuyển truy vấn đến chuyên gia | Không có |
| **Employee Search Agent** | Tìm đồng nghiệp và thành viên nhóm | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Tạo lộ trình học và đề xuất | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Tạo mẫu mã và hướng dẫn | Không có |

Quy trình cho phép:
- Triage → Bất kỳ chuyên gia nào
- Chuyên gia → Chuyên gia khác (cho các truy vấn liên quan)
- Chuyên gia → Triage (cho các chủ đề mới)

## Khắc phục sự cố

### Agent không phản hồi
- Xác nhận hosted agent đã được triển khai và đang chạy trong Azure AI Foundry
- Kiểm tra `HOSTED_AGENT_NAME` và `HOSTED_AGENT_VERSION` có khớp với triển khai của bạn không

### Lỗi vector store
- Đảm bảo `VECTOR_STORE_ID` được thiết lập chính xác
- Xác nhận vector store chứa dữ liệu nhân viên

### Lỗi xác thực
- Chạy `az login` để làm mới thông tin đăng nhập
- Đảm bảo bạn có quyền truy cập vào dự án Azure AI Foundry

## Tài nguyên

- [Tài liệu Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Mẫu tích hợp ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Tuyên bố từ chối trách nhiệm**:  
Tài liệu này đã được dịch bằng dịch vụ dịch thuật AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mặc dù chúng tôi cố gắng đảm bảo độ chính xác, xin lưu ý rằng các bản dịch tự động có thể chứa lỗi hoặc không chính xác. Tài liệu gốc bằng ngôn ngữ gốc nên được coi là nguồn tham khảo chính thức. Đối với các thông tin quan trọng, nên sử dụng dịch vụ dịch thuật chuyên nghiệp do con người thực hiện. Chúng tôi không chịu trách nhiệm về bất kỳ sự hiểu lầm hoặc giải thích sai nào phát sinh từ việc sử dụng bản dịch này.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->