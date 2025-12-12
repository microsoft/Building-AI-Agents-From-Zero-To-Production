<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:45:08+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "hr"
}
-->
# Sljedeći koraci nakon `azd init`

## Sadržaj

1. [Sljedeći koraci](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisioniranje infrastrukture](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Izmjena infrastrukture](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Priprema za produkciju](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Naplate](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Rješavanje problema](../../../../lesson-4-agentdeployment/hosted-agent)

## Sljedeći koraci

### Provisioniranje infrastrukture i implementacija koda aplikacije

Pokrenite `azd up` za provisioniranje vaše infrastrukture i implementaciju u Azure u jednom koraku (ili pokrenite `azd provision` pa `azd deploy` da obavite zadatke zasebno). Posjetite navedene krajnje točke usluge da vidite vašu aplikaciju u radu!

Za rješavanje problema pogledajte [rješavanje problema](../../../../lesson-4-agentdeployment/hosted-agent).

### Izmjena infrastrukture

Za opis infrastrukture i aplikacije dodan je `azure.yaml`. Ova datoteka sadrži sve usluge i resurse koji opisuju vašu aplikaciju.

Za dodavanje novih usluga ili resursa pokrenite `azd add`. Također možete izravno uređivati datoteku `azure.yaml` ako je potrebno.

### Priprema za produkciju

Kada je potrebno, `azd` generira potrebnu infrastrukturu kao kod u memoriji i koristi je. Ako želite vidjeti ili izmijeniti infrastrukturu koju `azd` koristi, pokrenite `azd infra gen` da je spremite na disk.

Ako to učinite, stvorit će se dodatni direktoriji:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Napomena*: Nakon što generirate infrastrukturu na disku, te datoteke su izvor istine za azd. Sve promjene napravljene u `azure.yaml` (kao što je kroz `azd add`) neće se odraziti u infrastrukturi dok je ponovno ne generirate s `azd infra gen`. Bit ćete upitani prije prepisivanja datoteka. Možete proslijediti `--force` da prisilite `azd infra gen` da prepiše datoteke bez upita.

Na kraju, pokrenite `azd pipeline config` za konfiguraciju CI/CD deployment pipeline-a.

## Naplate

Posjetite stranicu *Cost Management + Billing* u Azure Portalu za praćenje trenutnih troškova. Za više informacija o načinu naplate i kako možete pratiti troškove nastale u vašim Azure pretplatama, posjetite [pregled naplate](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Rješavanje problema

P: Posjetio/la sam navedenu krajnju točku usluge i vidim praznu stranicu, generičku početnu stranicu ili stranicu s greškom.

O: Vaša usluga možda nije uspjela pokrenuti se ili joj nedostaju neka konfiguracijska podešavanja. Za daljnju istragu:

1. Pokrenite `azd show`. Kliknite na poveznicu pod "View in Azure Portal" da otvorite grupu resursa u Azure Portalu.
2. Navigirajte do specifične Container App usluge koja ne uspijeva implementirati se.
3. Kliknite na neuspjelu reviziju pod "Revisions with Issues".
4. Pregledajte "Status details" za više informacija o vrsti neuspjeha.
5. Promatrajte izlaze logova iz Console log stream i System log stream da identificirate eventualne greške.
6. Ako se logovi zapisuju na disk, koristite *Console* u navigaciji za povezivanje na shell unutar pokrenutog kontejnera.

Za više informacija o rješavanju problema posjetite [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Dodatne informacije

Za dodatne informacije o postavljanju vašeg `azd` projekta, posjetite naše službene [dokumente](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Odricanje od odgovornosti**:
Ovaj dokument je preveden korištenjem AI usluge za prevođenje [Co-op Translator](https://github.com/Azure/co-op-translator). Iako nastojimo postići točnost, imajte na umu da automatski prijevodi mogu sadržavati pogreške ili netočnosti. Izvorni dokument na izvornom jeziku treba smatrati autoritativnim izvorom. Za kritične informacije preporučuje se profesionalni ljudski prijevod. Ne snosimo odgovornost za bilo kakva nesporazuma ili pogrešna tumačenja koja proizlaze iz korištenja ovog prijevoda.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->