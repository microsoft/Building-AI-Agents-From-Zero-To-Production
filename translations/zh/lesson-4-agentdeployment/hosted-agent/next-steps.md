<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:28:07+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "zh"
}
-->
# `azd init` 之后的下一步

## 目录

1. [下一步](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [配置基础设施](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [修改基础设施](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [达到生产就绪](../../../../lesson-4-agentdeployment/hosted-agent)
2. [计费](../../../../lesson-4-agentdeployment/hosted-agent)
3. [故障排除](../../../../lesson-4-agentdeployment/hosted-agent)

## 下一步

### 配置基础设施并部署应用代码

运行 `azd up` 以一步完成基础设施的配置和部署到 Azure（或者分别运行 `azd provision` 然后 `azd deploy` 来完成这些任务）。访问列出的服务端点，查看您的应用程序是否已启动运行！

如需排查任何问题，请参阅 [故障排除](../../../../lesson-4-agentdeployment/hosted-agent)。

### 修改基础设施

为了描述基础设施和应用，添加了 `azure.yaml` 文件。该文件包含描述您的应用的所有服务和资源。

要添加新的服务或资源，请运行 `azd add`。如果需要，您也可以直接编辑 `azure.yaml` 文件。

### 达到生产就绪

在需要时，`azd` 会在内存中生成所需的基础设施即代码并使用它。如果您想查看或修改 `azd` 使用的基础设施，请运行 `azd infra gen` 将其持久化到磁盘。

如果您这样做，将会创建一些额外的目录：

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*注意*：一旦您将基础设施生成到磁盘，这些文件就是 azd 的真实来源。对 `azure.yaml` 的任何更改（例如通过 `azd add`）都不会反映到基础设施中，除非您再次使用 `azd infra gen` 重新生成。它会在覆盖文件前提示您。您可以传递 `--force` 参数强制 `azd infra gen` 在不提示的情况下覆盖文件。

最后，运行 `azd pipeline config` 来配置 CI/CD 部署管道。

## 计费

访问 Azure 门户中的 *成本管理 + 计费* 页面以跟踪当前支出。有关计费方式以及如何监控 Azure 订阅中产生的费用的更多信息，请访问 [计费概述](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing)。

## 故障排除

问：我访问了列出的服务端点，看到的是空白页、通用欢迎页或错误页。

答：您的服务可能未能启动，或者缺少某些配置设置。进一步排查步骤：

1. 运行 `azd show`。点击“在 Azure 门户查看”下的链接以打开 Azure 门户中的资源组。
2. 导航到部署失败的特定容器应用服务。
3. 点击“有问题的修订版”下失败的修订版。
4. 查看“状态详情”以获取有关失败类型的更多信息。
5. 观察控制台日志流和系统日志流的日志输出，识别任何错误。
6. 如果日志写入磁盘，使用导航中的 *控制台* 连接到正在运行容器内的 shell。

有关更多故障排除信息，请访问 [容器应用故障排除](https://learn.microsoft.com/azure/container-apps/troubleshooting)。

### 其他信息

有关设置您的 `azd` 项目的更多信息，请访问我们的官方[文档](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert)。

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**免责声明**：  
本文件由人工智能翻译服务[Co-op Translator](https://github.com/Azure/co-op-translator)翻译而成。尽管我们力求准确，但请注意自动翻译可能包含错误或不准确之处。原始文件的母语版本应被视为权威来源。对于重要信息，建议使用专业人工翻译。因使用本翻译而产生的任何误解或误释，我们概不负责。
<!-- CO-OP TRANSLATOR DISCLAIMER END -->