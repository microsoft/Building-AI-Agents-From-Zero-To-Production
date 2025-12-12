<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:38:52+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "nl"
}
-->
# Volgende stappen na `azd init`

## Inhoudsopgave

1. [Volgende stappen](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Infrastructuur provisionen](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Infrastructuur aanpassen](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Productieklaar maken](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Facturering](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Probleemoplossing](../../../../lesson-4-agentdeployment/hosted-agent)

## Volgende stappen

### Infrastructuur provisionen en applicatiecode implementeren

Voer `azd up` uit om je infrastructuur te provisionen en in één stap naar Azure te implementeren (of voer eerst `azd provision` uit en daarna `azd deploy` om de taken afzonderlijk uit te voeren). Bezoek de vermelde service-eindpunten om je applicatie in werking te zien!

Voor het oplossen van problemen, zie [probleemoplossing](../../../../lesson-4-agentdeployment/hosted-agent).

### Infrastructuur aanpassen

Om de infrastructuur en applicatie te beschrijven, is `azure.yaml` toegevoegd. Dit bestand bevat alle services en resources die je applicatie beschrijven.

Om nieuwe services of resources toe te voegen, voer je `azd add` uit. Je kunt ook het `azure.yaml`-bestand direct bewerken indien nodig.

### Productieklaar maken

Indien nodig genereert `azd` de vereiste infrastructuur als code in het geheugen en gebruikt deze. Als je de infrastructuur die `azd` gebruikt wilt bekijken of aanpassen, voer dan `azd infra gen` uit om deze op schijf op te slaan.

Als je dit doet, worden er enkele extra mappen aangemaakt:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Opmerking*: Zodra je je infrastructuur naar schijf hebt gegenereerd, zijn die bestanden de bron van waarheid voor azd. Wijzigingen die in `azure.yaml` worden aangebracht (zoals via `azd add`) worden niet weerspiegeld in de infrastructuur totdat je deze opnieuw genereert met `azd infra gen`. Je krijgt een prompt voordat bestanden worden overschreven. Je kunt `--force` meegeven om `azd infra gen` te dwingen de bestanden zonder prompt te overschrijven.

Voer ten slotte `azd pipeline config` uit om een CI/CD-implementatiepipeline te configureren.

## Facturering

Bezoek de pagina *Kostenbeheer + Facturering* in de Azure Portal om de huidige uitgaven bij te houden. Voor meer informatie over hoe je wordt gefactureerd en hoe je de kosten in je Azure-abonnementen kunt monitoren, bezoek [factureringsoverzicht](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Probleemoplossing

V: Ik heb het vermelde service-eindpunt bezocht en zie een lege pagina, een generieke welkomstpagina of een foutpagina.

A: Je service is mogelijk niet gestart of er ontbreken configuratie-instellingen. Om verder te onderzoeken:

1. Voer `azd show` uit. Klik op de link onder "View in Azure Portal" om de resourcegroep te openen in Azure Portal.
2. Navigeer naar de specifieke Container App-service die niet wordt geïmplementeerd.
3. Klik op de mislukte revisie onder "Revisions with Issues".
4. Bekijk "Status details" voor meer informatie over het type fout.
5. Bekijk de loguitvoer van Console log stream en System log stream om eventuele fouten te identificeren.
6. Als logs naar schijf worden geschreven, gebruik dan *Console* in de navigatie om verbinding te maken met een shell binnen de draaiende container.

Voor meer informatie over probleemoplossing, bezoek [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Aanvullende informatie

Voor aanvullende informatie over het opzetten van je `azd`-project, bezoek onze officiële [documentatie](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:  
Dit document is vertaald met behulp van de AI-vertalingsdienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet als de gezaghebbende bron worden beschouwd. Voor cruciale informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->