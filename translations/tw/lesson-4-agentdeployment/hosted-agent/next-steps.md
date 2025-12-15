<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:29:21+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "tw"
}
-->
# Next Steps after `azd init`

## 目錄

1. [下一步](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [佈建基礎架構](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [修改基礎架構](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [準備生產環境](../../../../lesson-4-agentdeployment/hosted-agent)
2. [計費](../../../../lesson-4-agentdeployment/hosted-agent)
3. [疑難排解](../../../../lesson-4-agentdeployment/hosted-agent)

## 下一步

### 佈建基礎架構並部署應用程式程式碼

執行 `azd up` 以一步完成佈建基礎架構並部署到 Azure（或分別執行 `azd provision` 然後 `azd deploy` 來完成這些任務）。造訪列出的服務端點，即可看到您的應用程式正在運行！

如需疑難排解，請參閱 [疑難排解](../../../../lesson-4-agentdeployment/hosted-agent)。

### 修改基礎架構

為了描述基礎架構和應用程式，已新增 `azure.yaml`。此檔案包含描述您的應用程式的所有服務和資源。

若要新增服務或資源，請執行 `azd add`。如有需要，您也可以直接編輯 `azure.yaml` 檔案。

### 準備生產環境

在需要時，`azd` 會在記憶體中產生所需的基礎架構即程式碼並使用它。如果您想查看或修改 `azd` 使用的基礎架構，請執行 `azd infra gen` 將其保存到磁碟。

如果您這麼做，將會建立一些額外的目錄：

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*注意*：一旦您將基礎架構產生到磁碟，這些檔案即成為 azd 的真實來源。對 `azure.yaml` 所做的任何變更（例如透過 `azd add`）將不會反映在基礎架構中，除非您再次使用 `azd infra gen` 重新產生。系統會在覆寫檔案前提示您。您可以傳遞 `--force` 參數以強制 `azd infra gen` 覆寫檔案而不提示。

最後，執行 `azd pipeline config` 以設定 CI/CD 部署管線。

## 計費

造訪 Azure 入口網站中的 *成本管理 + 計費* 頁面以追蹤目前支出。欲了解更多關於您的計費方式，以及如何監控 Azure 訂閱中產生的費用，請造訪 [計費概觀](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing)。

## 疑難排解

問：我造訪了列出的服務端點，但看到空白頁面、通用歡迎頁面或錯誤頁面。

答：您的服務可能未能啟動，或缺少某些設定。進一步調查方法：

1. 執行 `azd show`。點擊「在 Azure 入口網站中檢視」下的連結以開啟 Azure 入口網站中的資源群組。
2. 導覽至部署失敗的特定 Container App 服務。
3. 點擊「有問題的修訂版本」下的失敗修訂版本。
4. 查看「狀態詳細資料」以取得失敗類型的更多資訊。
5. 觀察「主控台日誌串流」和「系統日誌串流」的日誌輸出，以識別任何錯誤。
6. 如果日誌寫入磁碟，請使用導覽中的 *主控台* 連接到正在執行容器內的 shell。

欲了解更多疑難排解資訊，請造訪 [Container Apps 疑難排解](https://learn.microsoft.com/azure/container-apps/troubleshooting)。

### 額外資訊

如需有關設定您的 `azd` 專案的更多資訊，請造訪我們的官方 [文件](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert)。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件係使用 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保翻譯的準確性，但請注意，自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而產生的任何誤解或誤譯負責。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->