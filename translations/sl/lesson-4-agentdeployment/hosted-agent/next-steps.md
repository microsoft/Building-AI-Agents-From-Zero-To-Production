<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:45:34+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "sl"
}
-->
# Naslednji koraki po `azd init`

## Kazalo

1. [Naslednji koraki](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Priprava infrastrukture](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Sprememba infrastrukture](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Priprava na produkcijo](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Zaračunavanje](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Odpravljanje težav](../../../../lesson-4-agentdeployment/hosted-agent)

## Naslednji koraki

### Priprava infrastrukture in nameščanje kode aplikacije

Zaženite `azd up`, da v enem koraku pripravite infrastrukturo in namestite v Azure (ali zaženite `azd provision` in nato `azd deploy`, da opravite naloge ločeno). Obiščite navedene končne točke storitev, da vidite svojo aplikacijo v teku!

Za odpravljanje težav glejte [odpravljanje težav](../../../../lesson-4-agentdeployment/hosted-agent).

### Sprememba infrastrukture

Za opis infrastrukture in aplikacije je bila dodana datoteka `azure.yaml`. Ta datoteka vsebuje vse storitve in vire, ki opisujejo vašo aplikacijo.

Za dodajanje novih storitev ali virov zaženite `azd add`. Po potrebi lahko tudi neposredno uredite datoteko `azure.yaml`.

### Priprava na produkcijo

Ko je potrebno, `azd` generira zahtevano infrastrukturo kot kodo v pomnilniku in jo uporablja. Če želite videti ali spremeniti infrastrukturo, ki jo `azd` uporablja, zaženite `azd infra gen`, da jo shranite na disk.

Če to storite, bodo ustvarjene dodatne mape:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Opomba*: Ko enkrat generirate infrastrukturo na disk, so te datoteke vir resnice za azd. Vsake spremembe v `azure.yaml` (na primer preko `azd add`) ne bodo odražene v infrastrukturi, dokler je ne regenerirate z `azd infra gen`. Pred prepisovanjem datotek vas bo opozoril. Lahko uporabite `--force`, da prisilite `azd infra gen` k prepisu datotek brez opozorila.

Na koncu zaženite `azd pipeline config`, da konfigurirate CI/CD cevovod za nameščanje.

## Zaračunavanje

Obiščite stran *Upravljanje stroškov + zaračunavanje* v Azure Portalu, da spremljate trenutne stroške. Za več informacij o tem, kako vam zaračunavajo, in kako lahko spremljate stroške v svojih Azure naročninah, obiščite [pregled zaračunavanja](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Odpravljanje težav

V: Obiskal sem navedeno končno točko storitve in vidim prazno stran, splošno pozdravno stran ali stran z napako.

O: Vaša storitev morda ni uspela zagnati ali pa ji manjkajo nekatere nastavitve konfiguracije. Za nadaljnjo preiskavo:

1. Zaženite `azd show`. Kliknite na povezavo pod "Ogled v Azure Portalu", da odprete skupino virov v Azure Portalu.
2. Pomaknite se do določene storitve Container App, ki se ne uspe namestiti.
3. Kliknite na neuspešno revizijo pod "Revizije z napakami".
4. Preglejte "Podrobnosti stanja" za več informacij o vrsti napake.
5. Opazujte izpise dnevnikov iz Console log stream in System log stream, da prepoznate morebitne napake.
6. Če se dnevniki zapisujejo na disk, uporabite *Console* v navigaciji, da se povežete na lupino znotraj delujočega kontejnerja.

Za več informacij o odpravljanju težav obiščite [odpravljanje težav Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Dodatne informacije

Za dodatne informacije o nastavitvi vašega projekta `azd` obiščite naše uradne [dokumente](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Omejitev odgovornosti**:
Ta dokument je bil preveden z uporabo storitve za prevajanje z umetno inteligenco [Co-op Translator](https://github.com/Azure/co-op-translator). Čeprav si prizadevamo za natančnost, vas opozarjamo, da avtomatizirani prevodi lahko vsebujejo napake ali netočnosti. Izvirni dokument v njegovem izvirnem jeziku velja za avtoritativni vir. Za ključne informacije priporočamo strokovni človeški prevod. Za morebitna nesporazume ali napačne interpretacije, ki izhajajo iz uporabe tega prevoda, ne odgovarjamo.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->