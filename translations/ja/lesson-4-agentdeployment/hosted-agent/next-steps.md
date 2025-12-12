<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:29:48+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "ja"
}
-->
# `azd init` の次のステップ

## 目次

1. [次のステップ](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [インフラストラクチャのプロビジョニング](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [インフラストラクチャの変更](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [本番環境準備](../../../../lesson-4-agentdeployment/hosted-agent)
2. [請求](../../../../lesson-4-agentdeployment/hosted-agent)
3. [トラブルシューティング](../../../../lesson-4-agentdeployment/hosted-agent)

## 次のステップ

### インフラストラクチャのプロビジョニングとアプリケーションコードのデプロイ

`azd up` を実行して、インフラストラクチャのプロビジョニングと Azure へのデプロイを一度に行います（または `azd provision` を実行してから `azd deploy` を実行して、タスクを別々に実行します）。リストされたサービスエンドポイントにアクセスして、アプリケーションが稼働していることを確認してください！

問題が発生した場合は、[トラブルシューティング](../../../../lesson-4-agentdeployment/hosted-agent) を参照してください。

### インフラストラクチャの変更

インフラストラクチャとアプリケーションを記述するために、`azure.yaml` が追加されました。このファイルには、アプリケーションを記述するすべてのサービスとリソースが含まれています。

新しいサービスやリソースを追加するには、`azd add` を実行します。必要に応じて `azure.yaml` ファイルを直接編集することもできます。

### 本番環境準備

必要に応じて、`azd` は必要なインフラストラクチャをコードとしてメモリ上で生成し、それを使用します。`azd` が使用するインフラストラクチャを確認または変更したい場合は、`azd infra gen` を実行してディスクに永続化してください。

これを行うと、いくつかの追加ディレクトリが作成されます：

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*注意*: インフラストラクチャをディスクに生成した後は、それらのファイルが `azd` の真のソースとなります。`azure.yaml` に加えた変更（`azd add` を通じて行ったものなど）は、再度 `azd infra gen` を実行してインフラストラクチャを再生成するまで反映されません。ファイルを上書きする前に確認のプロンプトが表示されます。`--force` を渡すと、プロンプトなしでファイルを強制的に上書きできます。

最後に、`azd pipeline config` を実行して CI/CD デプロイメントパイプラインを構成します。

## 請求

Azure ポータルの *コスト管理 + 請求* ページを訪れて、現在の支出を追跡してください。請求方法や Azure サブスクリプションで発生したコストの監視方法の詳細については、[請求の概要](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing) をご覧ください。

## トラブルシューティング

Q: リストされたサービスエンドポイントにアクセスしたところ、空白ページ、一般的なウェルカムページ、またはエラーページが表示されます。

A: サービスの起動に失敗しているか、設定が不足している可能性があります。詳細を調査するには：

1. `azd show` を実行します。「Azure ポータルで表示」のリンクをクリックして、Azure ポータルでリソースグループを開きます。
2. デプロイに失敗している特定のコンテナーアプリサービスに移動します。
3. 「問題のあるリビジョン」から失敗しているリビジョンをクリックします。
4. 「ステータスの詳細」を確認して、失敗の種類を把握します。
5. コンソールログストリームとシステムログストリームのログ出力を観察してエラーを特定します。
6. ログがディスクに書き込まれている場合は、ナビゲーションの *Console* を使って実行中のコンテナー内のシェルに接続します。

詳細なトラブルシューティング情報については、[Container Apps トラブルシューティング](https://learn.microsoft.com/azure/container-apps/troubleshooting) をご覧ください。

### 追加情報

`azd` プロジェクトのセットアップに関する追加情報は、公式の[ドキュメント](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert)をご覧ください。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責事項**：  
本書類はAI翻訳サービス「Co-op Translator」（https://github.com/Azure/co-op-translator）を使用して翻訳されました。正確性の向上に努めておりますが、自動翻訳には誤りや不正確な部分が含まれる可能性があります。原文の言語による文書が正式な情報源とみなされるべきです。重要な情報については、専門の人間による翻訳を推奨します。本翻訳の利用により生じたいかなる誤解や誤訳についても、当方は責任を負いかねます。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->