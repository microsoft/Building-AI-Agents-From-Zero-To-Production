<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T18:56:09+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ja"
}
-->
# レッスン 4: Azure AI Foundry ホステッドエージェント + ChatKit を使ったエージェントのデプロイ

このレッスンでは、マルチエージェントワークフローを Azure AI Foundry にホステッドエージェントとしてデプロイし、それと対話するための ChatKit ベースのフロントエンドを作成する方法を示します。

## アーキテクチャ

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

1. **North Central US リージョンの Azure AI Foundry プロジェクト**
2. **認証済みの Azure CLI** (`az login`)
3. **Azure Developer CLI** (`azd`) がインストールされていること
4. **Python 3.12+** と **Node.js 18+**
5. 従業員データで作成された **ベクターストア**

## クイックスタート

### 1. 環境変数の設定

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Azure AI Foundry プロジェクトの詳細で .env を編集してください
```

### 2. ホステッドエージェントのデプロイ

**オプション A: Azure Developer CLI を使用（推奨）**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**オプション B: Docker + Azure Container Registry を使用**

```bash
cd hosted-agent

# コンテナをビルドする
docker build -t developer-onboarding-agent:latest .

# ACR用のタグ
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACRにプッシュする
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI FoundryポータルまたはSDKを介してデプロイする
```

### 3. ChatKit バックエンドの起動

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

サーバーは `http://localhost:8001` で起動します

### 4. ChatKit フロントエンドの起動

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

フロントエンドは `http://localhost:3000` で起動します

### 5. アプリケーションのテスト

ブラウザで `http://localhost:3000` を開き、以下のクエリを試してください：

**従業員検索:**
- 「私は新しく入社しました！Microsoft で働いたことがある人はいますか？」
- 「Azure Functions の経験がある人は誰ですか？」

**学習リソース:**
- 「Kubernetes の学習パスを作成してください」
- 「クラウドアーキテクチャのために取得すべき認定資格は何ですか？」

**コーディング支援:**
- 「CosmosDB に接続する Python コードを書いてください」
- 「Azure Function の作成方法を教えてください」

**マルチエージェントクエリ:**
- 「クラウドエンジニアとして始めます。誰とつながり、何を学ぶべきですか？」

## プロジェクト構成

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

## マルチエージェントワークフロー

ホステッドエージェントは **HandoffBuilder** を使って4つの専門エージェントをオーケストレーションします：

| エージェント | 役割 | ツール |
|--------------|------|--------|
| **トリアージエージェント** | コーディネーター - クエリを専門家にルーティング | なし |
| **従業員検索エージェント** | 同僚やチームメンバーを検索 | HostedFileSearchTool (ベクターストア) |
| **学習エージェント** | 学習パスと推奨を作成 | HostedMCPTool (Microsoft Learn) |
| **コーディングエージェント** | コードサンプルとガイダンスを生成 | なし |

ワークフローは以下を可能にします：
- トリアージ → 任意の専門家
- 専門家 → 他の専門家（関連クエリのため）
- 専門家 → トリアージ（新しいトピックのため）

## トラブルシューティング

### エージェントが応答しない場合
- ホステッドエージェントが Azure AI Foundry にデプロイされて稼働しているか確認
- `HOSTED_AGENT_NAME` と `HOSTED_AGENT_VERSION` がデプロイと一致しているか確認

### ベクターストアのエラー
- `VECTOR_STORE_ID` が正しく設定されているか確認
- ベクターストアに従業員データが含まれているか確認

### 認証エラー
- `az login` を実行して資格情報を更新
- Azure AI Foundry プロジェクトへのアクセス権があるか確認

## リソース

- [Azure AI Foundry ホステッドエージェント ドキュメント](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ChatKit 統合サンプル](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：  
本書類はAI翻訳サービス「Co-op Translator」（https://github.com/Azure/co-op-translator）を使用して翻訳されました。正確性の向上に努めておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があります。原文の言語によるオリジナル文書が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や誤訳についても、当方は一切の責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->