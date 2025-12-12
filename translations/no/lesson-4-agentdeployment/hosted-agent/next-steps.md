<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:37:51+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "no"
}
-->
# Neste steg etter `azd init`

## Innholdsfortegnelse

1. [Neste steg](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionere infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Endre infrastruktur](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Komme til produksjonsklar](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fakturering](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Feilsøking](../../../../lesson-4-agentdeployment/hosted-agent)

## Neste steg

### Provisionere infrastruktur og distribuere applikasjonskode

Kjør `azd up` for å provisionere infrastrukturen din og distribuere til Azure i ett steg (eller kjør `azd provision` og deretter `azd deploy` for å utføre oppgavene separat). Besøk tjenesteendepunktene som er oppført for å se applikasjonen din i drift!

For å feilsøke eventuelle problemer, se [feilsøking](../../../../lesson-4-agentdeployment/hosted-agent).

### Endre infrastruktur

For å beskrive infrastrukturen og applikasjonen, ble `azure.yaml` lagt til. Denne filen inneholder alle tjenester og ressurser som beskriver applikasjonen din.

For å legge til nye tjenester eller ressurser, kjør `azd add`. Du kan også redigere `azure.yaml`-filen direkte om nødvendig.

### Komme til produksjonsklar

Når det trengs, genererer `azd` den nødvendige infrastrukturen som kode i minnet og bruker den. Hvis du ønsker å se eller endre infrastrukturen som `azd` bruker, kjør `azd infra gen` for å lagre den til disk.

Hvis du gjør dette, vil noen ekstra kataloger bli opprettet:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Merk*: Når du har generert infrastrukturen til disk, er disse filene sannhetskilden for azd. Eventuelle endringer gjort i `azure.yaml` (for eksempel gjennom `azd add`) vil ikke bli reflektert i infrastrukturen før du genererer den på nytt med `azd infra gen`. Du vil bli spurt før filene overskrives. Du kan bruke `--force` for å tvinge `azd infra gen` til å overskrive filene uten å spørre.

Til slutt, kjør `azd pipeline config` for å konfigurere en CI/CD distribusjonspipeline.

## Fakturering

Besøk siden *Cost Management + Billing* i Azure-portalen for å følge med på nåværende forbruk. For mer informasjon om hvordan du blir fakturert, og hvordan du kan overvåke kostnadene som påløper i dine Azure-abonnementer, besøk [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Feilsøking

Q: Jeg besøkte tjenesteendepunktet som er oppført, og jeg ser en blank side, en generell velkomstside eller en feilmelding.

A: Tjenesten din kan ha feilet ved oppstart, eller den kan mangle noen konfigurasjonsinnstillinger. For å undersøke nærmere:

1. Kjør `azd show`. Klikk på lenken under "View in Azure Portal" for å åpne ressursgruppen i Azure-portalen.
2. Naviger til den spesifikke Container App-tjenesten som feiler ved distribusjon.
3. Klikk på den feilede revisjonen under "Revisions with Issues".
4. Se gjennom "Status details" for mer informasjon om typen feil.
5. Observer loggutdata fra Console log stream og System log stream for å identifisere eventuelle feil.
6. Hvis logger skrives til disk, bruk *Console* i navigasjonen for å koble til et shell inne i den kjørende containeren.

For mer feilsøkingsinformasjon, besøk [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Tilleggsinformasjon

For mer informasjon om hvordan du setter opp ditt `azd`-prosjekt, besøk vår offisielle [dokumentasjon](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokumentet er oversatt ved hjelp av AI-oversettelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selv om vi streber etter nøyaktighet, vennligst vær oppmerksom på at automatiske oversettelser kan inneholde feil eller unøyaktigheter. Det opprinnelige dokumentet på originalspråket skal anses som den autoritative kilden. For kritisk informasjon anbefales profesjonell menneskelig oversettelse. Vi er ikke ansvarlige for eventuelle misforståelser eller feiltolkninger som oppstår ved bruk av denne oversettelsen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->