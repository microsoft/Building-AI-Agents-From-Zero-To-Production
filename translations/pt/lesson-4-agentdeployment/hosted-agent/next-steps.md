<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:33:36+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "pt"
}
-->
# Próximos Passos após `azd init`

## Índice

1. [Próximos Passos](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionar infraestrutura](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modificar infraestrutura](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Preparar para produção](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Faturação](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Resolução de Problemas](../../../../lesson-4-agentdeployment/hosted-agent)

## Próximos Passos

### Provisionar infraestrutura e implantar código da aplicação

Execute `azd up` para provisionar a sua infraestrutura e implantar no Azure num único passo (ou execute `azd provision` e depois `azd deploy` para realizar as tarefas separadamente). Visite os pontos finais do serviço listados para ver a sua aplicação a funcionar!

Para resolver quaisquer problemas, consulte [resolução de problemas](../../../../lesson-4-agentdeployment/hosted-agent).

### Modificar infraestrutura

Para descrever a infraestrutura e a aplicação, foi adicionado o ficheiro `azure.yaml`. Este ficheiro contém todos os serviços e recursos que descrevem a sua aplicação.

Para adicionar novos serviços ou recursos, execute `azd add`. Também pode editar diretamente o ficheiro `azure.yaml`, se necessário.

### Preparar para produção

Quando necessário, o `azd` gera a infraestrutura como código em memória e utiliza-a. Se quiser ver ou modificar a infraestrutura que o `azd` usa, execute `azd infra gen` para a persistir no disco.

Se fizer isto, serão criados alguns diretórios adicionais:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Nota*: Depois de gerar a sua infraestrutura para o disco, esses ficheiros são a fonte de verdade para o azd. Quaisquer alterações feitas ao `azure.yaml` (como através do `azd add`) não serão refletidas na infraestrutura até que a regenere com `azd infra gen` novamente. Será solicitado antes de sobrescrever os ficheiros. Pode usar `--force` para forçar o `azd infra gen` a sobrescrever os ficheiros sem pedir confirmação.

Por fim, execute `azd pipeline config` para configurar uma pipeline de implantação CI/CD.

## Faturação

Visite a página *Gestão de Custos + Faturação* no Portal Azure para acompanhar os gastos atuais. Para mais informações sobre como é faturado e como pode monitorizar os custos incorridos nas suas subscrições Azure, visite [visão geral da faturação](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Resolução de Problemas

P: Visitei o ponto final do serviço listado e estou a ver uma página em branco, uma página de boas-vindas genérica ou uma página de erro.

R: O seu serviço pode ter falhado ao iniciar ou pode estar a faltar algumas configurações. Para investigar mais a fundo:

1. Execute `azd show`. Clique no link em "Ver no Portal Azure" para abrir o grupo de recursos no Portal Azure.
2. Navegue até ao serviço Container App específico que está a falhar na implantação.
3. Clique na revisão com falha em "Revisões com Problemas".
4. Reveja os "Detalhes do estado" para mais informações sobre o tipo de falha.
5. Observe as saídas dos logs do Console log stream e System log stream para identificar quaisquer erros.
6. Se os logs forem escritos no disco, use *Console* na navegação para ligar a um shell dentro do contentor em execução.

Para mais informações de resolução de problemas, visite [Resolução de problemas do Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Informação adicional

Para mais informações sobre como configurar o seu projeto `azd`, visite a nossa documentação oficial [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:
Este documento foi traduzido utilizando o serviço de tradução automática [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, por favor tenha em conta que traduções automáticas podem conter erros ou imprecisões. O documento original na sua língua nativa deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se a tradução profissional humana. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações erradas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->