<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:34:00+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "br"
}
-->
# Próximos passos após `azd init`

## Índice

1. [Próximos passos](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionar infraestrutura](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modificar infraestrutura](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Preparar para produção](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Cobrança](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Solução de problemas](../../../../lesson-4-agentdeployment/hosted-agent)

## Próximos passos

### Provisionar infraestrutura e implantar código da aplicação

Execute `azd up` para provisionar sua infraestrutura e implantar no Azure em um único passo (ou execute `azd provision` e depois `azd deploy` para realizar as tarefas separadamente). Visite os endpoints do serviço listados para ver sua aplicação em funcionamento!

Para solucionar quaisquer problemas, veja [solução de problemas](../../../../lesson-4-agentdeployment/hosted-agent).

### Modificar infraestrutura

Para descrever a infraestrutura e a aplicação, foi adicionado o arquivo `azure.yaml`. Este arquivo contém todos os serviços e recursos que descrevem sua aplicação.

Para adicionar novos serviços ou recursos, execute `azd add`. Você também pode editar o arquivo `azure.yaml` diretamente, se necessário.

### Preparar para produção

Quando necessário, o `azd` gera a infraestrutura como código requerida na memória e a utiliza. Se você quiser ver ou modificar a infraestrutura que o `azd` usa, execute `azd infra gen` para persistir no disco.

Se fizer isso, alguns diretórios adicionais serão criados:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Nota*: Depois de gerar sua infraestrutura no disco, esses arquivos são a fonte de verdade para o azd. Quaisquer alterações feitas no `azure.yaml` (como por meio do `azd add`) não serão refletidas na infraestrutura até que você a regenere com `azd infra gen` novamente. Ele solicitará confirmação antes de sobrescrever os arquivos. Você pode passar `--force` para forçar o `azd infra gen` a sobrescrever os arquivos sem solicitar confirmação.

Por fim, execute `azd pipeline config` para configurar um pipeline de implantação CI/CD.

## Cobrança

Visite a página *Gerenciamento de Custos + Cobrança* no Portal do Azure para acompanhar os gastos atuais. Para mais informações sobre como você é cobrado e como pode monitorar os custos incorridos em suas assinaturas do Azure, visite [visão geral da cobrança](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Solução de problemas

P: Visitei o endpoint do serviço listado e estou vendo uma página em branco, uma página de boas-vindas genérica ou uma página de erro.

R: Seu serviço pode ter falhado ao iniciar ou pode estar faltando algumas configurações. Para investigar mais a fundo:

1. Execute `azd show`. Clique no link em "Visualizar no Portal do Azure" para abrir o grupo de recursos no Portal do Azure.
2. Navegue até o serviço específico do Container App que está falhando na implantação.
3. Clique na revisão com falha em "Revisões com Problemas".
4. Revise os "Detalhes do status" para mais informações sobre o tipo de falha.
5. Observe as saídas de log do Console log stream e System log stream para identificar quaisquer erros.
6. Se os logs forem gravados no disco, use o *Console* na navegação para conectar-se a um shell dentro do contêiner em execução.

Para mais informações de solução de problemas, visite [Solução de problemas do Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Informações adicionais

Para informações adicionais sobre como configurar seu projeto `azd`, visite nossa [documentação oficial](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->