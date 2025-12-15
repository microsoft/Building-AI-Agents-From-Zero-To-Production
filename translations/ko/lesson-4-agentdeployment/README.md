<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:56:48+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ko"
}
-->
# Lesson 4: Azure AI Foundry 호스티드 에이전트 + ChatKit을 사용한 에이전트 배포

이 수업에서는 다중 에이전트 워크플로우를 Azure AI Foundry에 호스티드 에이전트로 배포하고, 이를 상호작용할 수 있는 ChatKit 기반 프런트엔드를 만드는 방법을 보여줍니다.

## 아키텍처

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

## 사전 요구 사항

1. North Central US 지역의 **Azure AI Foundry 프로젝트**
2. 인증된 **Azure CLI** (`az login`)
3. 설치된 **Azure Developer CLI** (`azd`)
4. **Python 3.12+** 및 **Node.js 18+**
5. 직원 데이터로 생성된 **벡터 스토어**

## 빠른 시작

### 1. 환경 변수 설정

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Azure AI Foundry 프로젝트 세부 정보로 .env를 편집하세요
```

### 2. 호스티드 에이전트 배포

**옵션 A: Azure Developer CLI 사용 (권장)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**옵션 B: Docker + Azure Container Registry 사용**

```bash
cd hosted-agent

# 컨테이너 빌드
docker build -t developer-onboarding-agent:latest .

# ACR 태그
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR로 푸시
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry 포털 또는 SDK를 통해 배포
```

### 3. ChatKit 백엔드 시작

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # 윈도우에서: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

서버가 `http://localhost:8001`에서 시작됩니다.

### 4. ChatKit 프런트엔드 시작

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

프런트엔드가 `http://localhost:3000`에서 시작됩니다.

### 5. 애플리케이션 테스트

브라우저에서 `http://localhost:3000`을 열고 다음 쿼리를 시도해 보세요:

**직원 검색:**
- "저는 새로 왔어요! Microsoft에서 일한 사람이 있나요?"
- "Azure Functions 경험이 있는 사람은 누구인가요?"

**학습 자료:**
- "Kubernetes 학습 경로를 만들어 주세요"
- "클라우드 아키텍처를 위해 어떤 자격증을 취득해야 하나요?"

**코딩 도움:**
- "CosmosDB에 연결하는 Python 코드를 작성하는 데 도움을 주세요"
- "Azure Function 만드는 방법을 보여 주세요"

**다중 에이전트 쿼리:**
- "저는 클라우드 엔지니어로 시작합니다. 누구와 연결하고 무엇을 배워야 하나요?"

## 프로젝트 구조

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

## 다중 에이전트 워크플로우

호스티드 에이전트는 **HandoffBuilder**를 사용하여 네 개의 전문 에이전트를 조율합니다:

| 에이전트 | 역할 | 도구 |
|-------|------|-------|
| **Triage Agent** | 코디네이터 - 쿼리를 전문가에게 라우팅 | 없음 |
| **Employee Search Agent** | 동료 및 팀원 찾기 | HostedFileSearchTool (벡터 스토어) |
| **Learning Agent** | 학습 경로 및 추천 생성 | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | 코드 샘플 및 가이드 생성 | 없음 |

워크플로우는 다음을 허용합니다:
- Triage → 모든 전문가
- 전문가 → 다른 전문가 (관련 쿼리용)
- 전문가 → Triage (새 주제용)

## 문제 해결

### 에이전트가 응답하지 않을 때
- 호스티드 에이전트가 Azure AI Foundry에 배포되어 실행 중인지 확인하세요
- `HOSTED_AGENT_NAME`과 `HOSTED_AGENT_VERSION`이 배포와 일치하는지 확인하세요

### 벡터 스토어 오류
- `VECTOR_STORE_ID`가 올바르게 설정되었는지 확인하세요
- 벡터 스토어에 직원 데이터가 포함되어 있는지 확인하세요

### 인증 오류
- `az login`을 실행하여 자격 증명을 갱신하세요
- Azure AI Foundry 프로젝트에 접근 권한이 있는지 확인하세요

## 리소스

- [Azure AI Foundry 호스티드 에이전트 문서](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit 통합 샘플](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**면책 조항**:  
이 문서는 AI 번역 서비스 [Co-op Translator](https://github.com/Azure/co-op-translator)를 사용하여 번역되었습니다. 정확성을 위해 최선을 다하고 있으나, 자동 번역에는 오류나 부정확한 부분이 있을 수 있음을 유의하시기 바랍니다. 원문 문서가 권위 있는 출처로 간주되어야 합니다. 중요한 정보의 경우 전문적인 인간 번역을 권장합니다. 본 번역 사용으로 인한 오해나 잘못된 해석에 대해 당사는 책임을 지지 않습니다.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->