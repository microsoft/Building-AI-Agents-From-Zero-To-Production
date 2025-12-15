<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:47:27+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "lt"
}
-->
# Kiti veiksmai po `azd init`

## Turinys

1. [Kiti veiksmai](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Infrastruktūros paruošimas](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Infrastruktūros keitimas](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Pasiruošimas gamybai](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Apmokėjimas](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Trikčių šalinimas](../../../../lesson-4-agentdeployment/hosted-agent)

## Kiti veiksmai

### Infrastruktūros paruošimas ir programos kodo diegimas

Paleiskite `azd up`, kad vienu žingsniu paruoštumėte infrastruktūrą ir įdiegtumėte į Azure (arba paleiskite `azd provision`, o tada `azd deploy`, kad atliktumėte užduotis atskirai). Aplankykite nurodytus paslaugų galinius taškus, kad pamatytumėte savo veikiančią programą!

Norėdami išspręsti problemas, žr. [trikčių šalinimą](../../../../lesson-4-agentdeployment/hosted-agent).

### Infrastruktūros keitimas

Norint aprašyti infrastruktūrą ir programą, buvo pridėtas failas `azure.yaml`. Šiame faile yra visos paslaugos ir ištekliai, aprašantys jūsų programą.

Norėdami pridėti naujų paslaugų ar išteklių, paleiskite `azd add`. Taip pat galite tiesiogiai redaguoti failą `azure.yaml`, jei reikia.

### Pasiruošimas gamybai

Kai reikia, `azd` generuoja reikiamą infrastruktūrą kaip kodą atmintyje ir ją naudoja. Jei norite pamatyti arba pakeisti infrastruktūrą, kurią naudoja `azd`, paleiskite `azd infra gen`, kad ją išsaugotumėte diske.

Jei tai padarysite, bus sukurti papildomi katalogai:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Pastaba*: Kai infrastruktūrą sugeneruosite diske, tie failai taps pagrindiniu `azd` šaltiniu. Bet kokie pakeitimai faile `azure.yaml` (pvz., per `azd add`) nebus atspindėti infrastruktūroje, kol vėl jos neišgeneruosite su `azd infra gen`. Jis paprašys patvirtinimo prieš perrašant failus. Galite naudoti `--force`, kad priverstumėte `azd infra gen` perrašyti failus be patvirtinimo.

Galiausiai paleiskite `azd pipeline config`, kad sukonfigūruotumėte CI/CD diegimo vamzdyną.

## Apmokėjimas

Aplankykite *Cost Management + Billing* puslapį Azure portale, kad stebėtumėte esamas išlaidas. Daugiau informacijos apie apmokėjimą ir kaip galite stebėti išlaidas savo Azure prenumeratose rasite [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Trikčių šalinimas

K: Aplankiau nurodytą paslaugos galinį tašką ir matau tuščią puslapį, bendrą pasveikinimo puslapį arba klaidos puslapį.

A: Jūsų paslauga galėjo nepavykti paleisti arba trūksta kai kurių konfigūracijos nustatymų. Norėdami toliau tirti:

1. Paleiskite `azd show`. Spustelėkite nuorodą po „View in Azure Portal“, kad atidarytumėte išteklių grupę Azure portale.
2. Eikite į konkretų Container App paslaugą, kuri nepavyksta įdiegti.
3. Spustelėkite nepavykusį leidimą po „Revisions with Issues“.
4. Peržiūrėkite „Status details“, kad sužinotumėte daugiau apie gedimo tipą.
5. Stebėkite konsolės ir sistemos žurnalų srautus, kad identifikuotumėte klaidas.
6. Jei žurnalai rašomi į diską, naudokite *Console* navigacijoje, kad prisijungtumėte prie apvalkalo veikiančiame konteineryje.

Daugiau trikčių šalinimo informacijos rasite [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Papildoma informacija

Daugiau informacijos apie `azd` projekto nustatymą rasite mūsų oficialioje [dokumentacijoje](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Atsakomybės apribojimas**:
Šis dokumentas buvo išverstas naudojant dirbtinio intelekto vertimo paslaugą [Co-op Translator](https://github.com/Azure/co-op-translator). Nors siekiame tikslumo, prašome atkreipti dėmesį, kad automatiniai vertimai gali turėti klaidų ar netikslumų. Originalus dokumentas gimtąja kalba turėtų būti laikomas autoritetingu šaltiniu. Kritinei informacijai rekomenduojamas profesionalus žmogaus vertimas. Mes neatsakome už bet kokius nesusipratimus ar neteisingus aiškinimus, kilusius dėl šio vertimo naudojimo.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->