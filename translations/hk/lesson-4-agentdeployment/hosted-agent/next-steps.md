<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:28:53+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "hk"
}
-->
# Next Steps after `azd init`

## Table of Contents

1. [Next Steps](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provision infrastructure](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modify infrastructure](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Getting to production-ready](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Billing](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Troubleshooting](../../../../lesson-4-agentdeployment/hosted-agent)

## Next Steps

### Provision infrastructure and deploy application code

Run `azd up` to provision your infrastructure and deploy to Azure in one step (or run `azd provision` then `azd deploy` to accomplish the tasks separately). Visit the service endpoints listed to see your application up-and-running!

To troubleshoot any issues, see [troubleshooting](../../../../lesson-4-agentdeployment/hosted-agent).

### Modify infrastructure

To describe the infrastructure and application, `azure.yaml` was added. This file contains all services and resources that describe your application.

To add new services or resources, run `azd add`. You may also edit the `azure.yaml` file directly if needed.

### Getting to production-ready

When needed, `azd` generates the required infrastructure as code in memory and uses it. If you would like to see or modify the infrastructure that `azd` uses, run `azd infra gen` to persist it to disk.

If you do this, some additional directories will be created:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Note*: Once you have generated your infrastructure to disk, those files are the source of truth for azd. Any changes made to `azure.yaml` (such as through `azd add`) will not be reflected in the infrastructure until you regenerate it with `azd infra gen` again. It will prompt you before overwriting files. You can pass `--force` to force `azd infra gen` to overwrite the files without prompting.

Finally, run `azd pipeline config` to configure a CI/CD deployment pipeline.

## Billing

Visit the *Cost Management + Billing* page in Azure Portal to track current spend. For more information about how you're billed, and how you can monitor the costs incurred in your Azure subscriptions, visit [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Troubleshooting

Q: I visited the service endpoint listed, and I'm seeing a blank page, a generic welcome page, or an error page.

A: Your service may have failed to start, or it may be missing some configuration settings. To investigate further:

1. Run `azd show`. Click on the link under "View in Azure Portal" to open the resource group in Azure Portal.
2. Navigate to the specific Container App service that is failing to deploy.
3. Click on the failing revision under "Revisions with Issues".
4. Review "Status details" for more information about the type of failure.
5. Observe the log outputs from Console log stream and System log stream to identify any errors.
6. If logs are written to disk, use *Console* in the navigation to connect to a shell within the running container.

For more troubleshooting information, visit [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Additional information

For additional information about setting up your `azd` project, visit our official [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免責聲明**：  
本文件由 AI 翻譯服務 [Co-op Translator](https://github.com/Azure/co-op-translator) 進行翻譯。雖然我們致力於確保準確性，但請注意自動翻譯可能包含錯誤或不準確之處。原始文件的母語版本應被視為權威來源。對於重要資訊，建議採用專業人工翻譯。我們不對因使用本翻譯而引起的任何誤解或誤釋承擔責任。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->