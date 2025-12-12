<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:48:49+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "pcm"
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

Run `azd up` to provision your infrastructure and deploy to Azure for one step (or run `azd provision` then `azd deploy` to do the tasks separately). Visit the service endpoints wey dem list to see your application dey run!

To troubleshoot any wahala, see [troubleshooting](../../../../lesson-4-agentdeployment/hosted-agent).

### Modify infrastructure

To describe the infrastructure and application, `azure.yaml` dey added. This file get all services and resources wey describe your application.

To add new services or resources, run `azd add`. You fit also edit the `azure.yaml` file directly if you need.

### Getting to production-ready

When e necessary, `azd` dey generate the required infrastructure as code for memory and e dey use am. If you want see or modify the infrastructure wey `azd` dey use, run `azd infra gen` to save am for disk.

If you do this, some extra directories go dey created:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Note*: Once you don generate your infrastructure to disk, those files na the source of truth for azd. Any changes wey you make for `azure.yaml` (like through `azd add`) no go show for the infrastructure until you generate am again with `azd infra gen`. E go ask you before e overwrite files. You fit pass `--force` to make `azd infra gen` overwrite the files without asking.

Finally, run `azd pipeline config` to set up CI/CD deployment pipeline.

## Billing

Visit the *Cost Management + Billing* page for Azure Portal to track how you dey spend money now. For more info about how dem dey bill you, and how you fit monitor the costs wey your Azure subscriptions dey incur, visit [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Troubleshooting

Q: I visit the service endpoint wey dem list, and I dey see blank page, generic welcome page, or error page.

A: Your service fit no start well, or e fit dey miss some configuration settings. To check am well:

1. Run `azd show`. Click the link under "View in Azure Portal" to open the resource group for Azure Portal.
2. Go the specific Container App service wey no dey deploy well.
3. Click the failing revision under "Revisions with Issues".
4. Check "Status details" for more info about the kind failure.
5. Look the log outputs from Console log stream and System log stream to find any errors.
6. If logs dey write to disk, use *Console* for navigation to connect to shell inside the running container.

For more troubleshooting info, visit [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Additional information

For more info about how to set up your `azd` project, visit our official [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dis document na AI translation service [Co-op Translator](https://github.com/Azure/co-op-translator) wey dem use translate am. Even though we dey try make am correct, abeg sabi say automated translation fit get some mistakes or no too correct. The original document wey e dey for im own language na the correct one. If na serious matter, e better make person wey sabi translate am well well do am. We no go responsible for any wahala or wrong understanding wey fit happen because of this translation.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->