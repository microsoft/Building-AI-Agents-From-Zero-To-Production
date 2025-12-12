<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:34:26+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "it"
}
-->
# Passi successivi dopo `azd init`

## Indice

1. [Passi successivi](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionare l'infrastruttura](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modificare l'infrastruttura](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Prepararsi alla produzione](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fatturazione](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Risoluzione dei problemi](../../../../lesson-4-agentdeployment/hosted-agent)

## Passi successivi

### Provisionare l'infrastruttura e distribuire il codice dell'applicazione

Esegui `azd up` per provisionare la tua infrastruttura e distribuire su Azure in un unico passaggio (oppure esegui `azd provision` e poi `azd deploy` per completare le attività separatamente). Visita gli endpoint del servizio elencati per vedere la tua applicazione in esecuzione!

Per risolvere eventuali problemi, consulta [risoluzione dei problemi](../../../../lesson-4-agentdeployment/hosted-agent).

### Modificare l'infrastruttura

Per descrivere l'infrastruttura e l'applicazione, è stato aggiunto `azure.yaml`. Questo file contiene tutti i servizi e le risorse che descrivono la tua applicazione.

Per aggiungere nuovi servizi o risorse, esegui `azd add`. Puoi anche modificare direttamente il file `azure.yaml` se necessario.

### Prepararsi alla produzione

Quando necessario, `azd` genera l'infrastruttura richiesta come codice in memoria e la utilizza. Se desideri vedere o modificare l'infrastruttura che `azd` utilizza, esegui `azd infra gen` per salvarla su disco.

Se lo fai, verranno create alcune directory aggiuntive:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Nota*: Una volta generata l'infrastruttura su disco, quei file diventano la fonte di verità per azd. Qualsiasi modifica apportata a `azure.yaml` (ad esempio tramite `azd add`) non sarà riflessa nell'infrastruttura finché non la rigeneri con `azd infra gen` di nuovo. Ti verrà chiesto conferma prima di sovrascrivere i file. Puoi passare `--force` per forzare `azd infra gen` a sovrascrivere i file senza chiedere conferma.

Infine, esegui `azd pipeline config` per configurare una pipeline di distribuzione CI/CD.

## Fatturazione

Visita la pagina *Gestione costi + Fatturazione* nel Portale di Azure per monitorare la spesa attuale. Per maggiori informazioni su come vieni fatturato e su come puoi monitorare i costi sostenuti nelle tue sottoscrizioni Azure, visita [panoramica della fatturazione](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Risoluzione dei problemi

D: Ho visitato l'endpoint del servizio elencato e vedo una pagina vuota, una pagina di benvenuto generica o una pagina di errore.

R: Il tuo servizio potrebbe non essere partito correttamente o potrebbe mancare qualche impostazione di configurazione. Per indagare ulteriormente:

1. Esegui `azd show`. Clicca sul link sotto "Visualizza nel Portale di Azure" per aprire il gruppo di risorse nel Portale di Azure.
2. Naviga al servizio Container App specifico che non è riuscito a distribuire.
3. Clicca sulla revisione fallita sotto "Revisioni con problemi".
4. Controlla i "Dettagli stato" per maggiori informazioni sul tipo di errore.
5. Osserva gli output dei log da Console log stream e System log stream per identificare eventuali errori.
6. Se i log sono scritti su disco, usa *Console* nella navigazione per connetterti a una shell all'interno del container in esecuzione.

Per ulteriori informazioni sulla risoluzione dei problemi, visita [Risoluzione problemi Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Informazioni aggiuntive

Per ulteriori informazioni sulla configurazione del tuo progetto `azd`, visita la nostra documentazione ufficiale [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Questo documento è stato tradotto utilizzando il servizio di traduzione automatica [Co-op Translator](https://github.com/Azure/co-op-translator). Pur impegnandoci per garantire l’accuratezza, si prega di notare che le traduzioni automatiche possono contenere errori o imprecisioni. Il documento originale nella sua lingua nativa deve essere considerato la fonte autorevole. Per informazioni critiche, si raccomanda una traduzione professionale effettuata da un traduttore umano. Non ci assumiamo alcuna responsabilità per eventuali malintesi o interpretazioni errate derivanti dall’uso di questa traduzione.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->