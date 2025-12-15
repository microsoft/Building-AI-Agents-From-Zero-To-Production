<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:37:23+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "da"
}
-->
# Næste skridt efter `azd init`

## Indholdsfortegnelse

1. [Næste skridt](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionér infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Ændr infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Klar til produktion](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fakturering](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Fejlfinding](../../../../lesson-4-agentdeployment/hosted-agent)

## Næste skridt

### Provisionér infrastruktur og deploy applikationskode

Kør `azd up` for at provisionere din infrastruktur og deploye til Azure i ét trin (eller kør `azd provision` og derefter `azd deploy` for at udføre opgaverne separat). Besøg de listede serviceendpoints for at se din applikation kørende!

For at fejlfinde eventuelle problemer, se [fejlfinding](../../../../lesson-4-agentdeployment/hosted-agent).

### Ændr infrastruktur

For at beskrive infrastrukturen og applikationen blev `azure.yaml` tilføjet. Denne fil indeholder alle services og ressourcer, der beskriver din applikation.

For at tilføje nye services eller ressourcer, kør `azd add`. Du kan også redigere `azure.yaml`-filen direkte, hvis nødvendigt.

### Klar til produktion

Når det er nødvendigt, genererer `azd` den krævede infrastruktur som kode i hukommelsen og bruger den. Hvis du ønsker at se eller ændre den infrastruktur, som `azd` bruger, kan du køre `azd infra gen` for at gemme den på disk.

Hvis du gør dette, vil nogle ekstra mapper blive oprettet:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Bemærk*: Når du har genereret din infrastruktur til disk, er disse filer sandhedskilden for azd. Ændringer foretaget i `azure.yaml` (såsom via `azd add`) vil ikke blive reflekteret i infrastrukturen, før du genererer den igen med `azd infra gen`. Du vil blive spurgt, før filer overskrives. Du kan bruge `--force` for at tvinge `azd infra gen` til at overskrive filerne uden at spørge.

Afslutningsvis, kør `azd pipeline config` for at konfigurere en CI/CD deploymentspipeline.

## Fakturering

Besøg siden *Cost Management + Billing* i Azure Portal for at følge det aktuelle forbrug. For mere information om, hvordan du bliver faktureret, og hvordan du kan overvåge omkostningerne i dine Azure-abonnementer, besøg [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Fejlfinding

Q: Jeg besøgte det listede serviceendpoint, og jeg ser en tom side, en generisk velkomstside eller en fejlside.

A: Din service kan være fejlet i opstarten, eller den kan mangle nogle konfigurationsindstillinger. For at undersøge nærmere:

1. Kør `azd show`. Klik på linket under "View in Azure Portal" for at åbne ressourcegruppen i Azure Portal.
2. Naviger til den specifikke Container App-service, der fejler i deployment.
3. Klik på den fejlede revision under "Revisions with Issues".
4. Gennemgå "Status details" for mere information om typen af fejl.
5. Observer logudskrifterne fra Console log stream og System log stream for at identificere eventuelle fejl.
6. Hvis logs skrives til disk, brug *Console* i navigationen for at forbinde til en shell inden i den kørende container.

For mere fejlfinding, besøg [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Yderligere information

For yderligere information om opsætning af dit `azd`-projekt, besøg vores officielle [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, bedes du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det oprindelige dokument på dets modersmål bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->