<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:48:27+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "et"
}
-->
# Järgmised sammud pärast `azd init`

## Sisukord

1. [Järgmised sammud](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Taristu loomine](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Taristu muutmine](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Tootmiskõlblikuks saamine](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Arveldamine](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Tõrkeotsing](../../../../lesson-4-agentdeployment/hosted-agent)

## Järgmised sammud

### Taristu loomine ja rakenduskoodi juurutamine

Käivitage `azd up`, et luua taristu ja juurutada Azure’i ühes etapis (või käivitage eraldi ülesannete täitmiseks `azd provision` ja seejärel `azd deploy`). Külastage loetletud teenuse lõpp-punkte, et näha oma rakendust töös!

Tõrkeotsingu jaoks vaadake [tõrkeotsingut](../../../../lesson-4-agentdeployment/hosted-agent).

### Taristu muutmine

Rakenduse ja taristu kirjeldamiseks lisati fail `azure.yaml`. See fail sisaldab kõiki teenuseid ja ressursse, mis kirjeldavad teie rakendust.

Uute teenuste või ressursside lisamiseks käivitage `azd add`. Vajadusel võite ka otse faili `azure.yaml` muuta.

### Tootmiskõlblikuks saamine

Vajadusel genereerib `azd` vajaliku infrastruktuuri koodi mälus ja kasutab seda. Kui soovite näha või muuta infrastruktuuri, mida `azd` kasutab, käivitage `azd infra gen`, et see kettale salvestada.

Kui teete seda, luuakse mõned täiendavad kataloogid:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Märkus*: Kui olete infrastruktuuri kettale genereerinud, on need failid `azd` jaoks tõeallikaks. Kõik `azure.yaml`-s tehtud muudatused (näiteks `azd add` kaudu) ei kajastu infrastruktuuris enne, kui te selle uuesti genereerite käsuga `azd infra gen`. See küsib enne failide ülekirjutamist luba. Võite kasutada `--force`, et sundida `azd infra gen` failid ilma kinnitust küsimata üle kirjutama.

Lõpuks käivitage `azd pipeline config`, et seadistada CI/CD juurutustoru.

## Arveldamine

Jälgige jooksvaid kulutusi Azure’i portaali lehel *Cost Management + Billing*. Lisateavet arveldamise kohta ja selle kohta, kuidas saate jälgida oma Azure’i tellimustes tekkinud kulusid, leiate lehelt [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Tõrkeotsing

K: Külastasin loetletud teenuse lõpp-punkti ja näen tühja lehte, üldist tervituslehte või vealehte.

V: Teie teenus ei pruukinud käivituda või võib puududa mõni konfiguratsiooniseade. Täpsemaks uurimiseks:

1. Käivitage `azd show`. Klõpsake lingil "View in Azure Portal", et avada ressursigrupp Azure’i portaalis.
2. Navigeerige konkreetse konteinerirakenduse teenuseni, mis ei õnnestunud juurutada.
3. Klõpsake ebaõnnestunud revisjonil jaotises "Revisions with Issues".
4. Vaadake "Status details", et saada rohkem teavet tõrke tüübi kohta.
5. Vaadake konsooli logi ja süsteemi logi vooge, et tuvastada vead.
6. Kui logid kirjutatakse kettale, kasutage navigeerimises *Console*, et ühendada jooksva konteineri sees olevasse shelli.

Lisateavet tõrkeotsingu kohta leiate lehelt [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Täiendav teave

Lisateavet `azd` projekti seadistamise kohta leiate meie ametlikust [dokumentatsioonist](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastutusest loobumine**:
See dokument on tõlgitud kasutades tehisintellekti tõlketeenust [Co-op Translator](https://github.com/Azure/co-op-translator). Kuigi püüame täpsust, palun arvestage, et automaatsed tõlked võivad sisaldada vigu või ebatäpsusi. Originaaldokument selle emakeeles tuleks pidada autoriteetseks allikaks. Olulise teabe puhul soovitatakse kasutada professionaalset inimtõlget. Me ei vastuta selle tõlke kasutamisest tulenevate arusaamatuste või valesti mõistmiste eest.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->