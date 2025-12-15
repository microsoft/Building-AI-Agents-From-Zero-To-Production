<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:36:59+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "sv"
}
-->
# Nästa steg efter `azd init`

## Innehållsförteckning

1. [Nästa steg](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionera infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modifiera infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Att bli produktionsklar](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fakturering](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Felsökning](../../../../lesson-4-agentdeployment/hosted-agent)

## Nästa steg

### Provisionera infrastruktur och distribuera applikationskod

Kör `azd up` för att provisionera din infrastruktur och distribuera till Azure i ett steg (eller kör `azd provision` och sedan `azd deploy` för att utföra uppgifterna separat). Besök de listade tjänsteendpunkterna för att se din applikation igång!

För att felsöka eventuella problem, se [felsökning](../../../../lesson-4-agentdeployment/hosted-agent).

### Modifiera infrastruktur

För att beskriva infrastrukturen och applikationen lades `azure.yaml` till. Denna fil innehåller alla tjänster och resurser som beskriver din applikation.

För att lägga till nya tjänster eller resurser, kör `azd add`. Du kan också redigera `azure.yaml`-filen direkt vid behov.

### Att bli produktionsklar

När det behövs genererar `azd` den nödvändiga infrastrukturen som kod i minnet och använder den. Om du vill se eller modifiera infrastrukturen som `azd` använder, kör `azd infra gen` för att spara den på disk.

Om du gör detta skapas några ytterligare kataloger:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Obs*: När du har genererat din infrastruktur till disk är dessa filer sanningskällan för azd. Eventuella ändringar som görs i `azure.yaml` (till exempel via `azd add`) kommer inte att återspeglas i infrastrukturen förrän du genererar den igen med `azd infra gen`. Du kommer att bli tillfrågad innan filer skrivs över. Du kan använda `--force` för att tvinga `azd infra gen` att skriva över filerna utan att fråga.

Avslutningsvis, kör `azd pipeline config` för att konfigurera en CI/CD-distributionspipeline.

## Fakturering

Besök sidan *Cost Management + Billing* i Azure Portal för att följa aktuell kostnad. För mer information om hur du faktureras och hur du kan övervaka kostnaderna i dina Azure-prenumerationer, besök [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Felsökning

F: Jag besökte den listade tjänsteendpunkten och ser en tom sida, en generisk välkomstsida eller en felsida.

S: Din tjänst kan ha misslyckats med att starta eller sakna vissa konfigurationsinställningar. För att undersöka vidare:

1. Kör `azd show`. Klicka på länken under "View in Azure Portal" för att öppna resursgruppen i Azure Portal.
2. Navigera till den specifika Container App-tjänsten som misslyckas med distributionen.
3. Klicka på den misslyckade revisionen under "Revisions with Issues".
4. Granska "Status details" för mer information om typen av fel.
5. Observera loggutdata från Console log stream och System log stream för att identifiera eventuella fel.
6. Om loggar skrivs till disk, använd *Console* i navigeringen för att ansluta till ett skal inom den körande containern.

För mer felsökningsinformation, besök [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Ytterligare information

För ytterligare information om hur du sätter upp ditt `azd`-projekt, besök vår officiella [dokumentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfriskrivning**:
Detta dokument har översatts med hjälp av AI-översättningstjänsten [Co-op Translator](https://github.com/Azure/co-op-translator). Även om vi strävar efter noggrannhet, vänligen observera att automatiska översättningar kan innehålla fel eller brister. Det ursprungliga dokumentet på dess modersmål bör betraktas som den auktoritativa källan. För kritisk information rekommenderas professionell mänsklig översättning. Vi ansvarar inte för några missförstånd eller feltolkningar som uppstår till följd av användningen av denna översättning.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->