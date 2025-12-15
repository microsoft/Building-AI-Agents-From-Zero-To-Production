<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:41:36+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "sw"
}
-->
# Hatua Zifuatazo baada ya `azd init`

## Jedwali la Yaliyomo

1. [Hatua Zifuatazo](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Kuweka miundombinu na kupeleka msimbo wa programu](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Kubadilisha miundombinu](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Kufikia hali ya uzalishaji](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Malipo](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Kutatua matatizo](../../../../lesson-4-agentdeployment/hosted-agent)

## Hatua Zifuatazo

### Kuweka miundombinu na kupeleka msimbo wa programu

Endesha `azd up` kuweka miundombinu yako na kupeleka kwenye Azure kwa hatua moja (au endesha `azd provision` kisha `azd deploy` kutekeleza kazi hizo kwa njia tofauti). Tembelea anwani za huduma zilizoorodheshwa kuona programu yako ikifanya kazi!

Ili kutatua matatizo yoyote, angalia [kutatua matatizo](../../../../lesson-4-agentdeployment/hosted-agent).

### Kubadilisha miundombinu

Ili kuelezea miundombinu na programu, `azure.yaml` iliongezwa. Faili hili lina huduma zote na rasilimali zinazofafanua programu yako.

Ili kuongeza huduma mpya au rasilimali, endesha `azd add`. Pia unaweza kuhariri faili ya `azure.yaml` moja kwa moja ikiwa inahitajika.

### Kufikia hali ya uzalishaji

Wakati inahitajika, `azd` hutengeneza miundombinu inayohitajika kama msimbo akilini na kuitumia. Ikiwa ungependa kuona au kubadilisha miundombinu ambayo `azd` hutumia, endesha `azd infra gen` kuihifadhi kwenye diski.

Ukifanya hivyo, baadhi ya saraka za ziada zitatengenezwa:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Kumbuka*: Mara tu utakapotengeneza miundombinu yako kwenye diski, faili hizo ndizo chanzo cha ukweli kwa azd. Mabadiliko yoyote yaliyofanywa kwenye `azure.yaml` (kama vile kupitia `azd add`) hayatatafsirika kwenye miundombinu hadi uizalishe tena kwa `azd infra gen`. Itakuuliza ruhusa kabla ya kuandika juu ya faili. Unaweza kutumia `--force` kulazimisha `azd infra gen` kuandika juu ya faili bila kuuliza.

Mwishowe, endesha `azd pipeline config` kusanidi njia ya utoaji wa CI/CD.

## Malipo

Tembelea ukurasa wa *Usimamizi wa Gharama + Malipo* katika Azure Portal kufuatilia matumizi ya sasa. Kwa maelezo zaidi kuhusu jinsi unavyolipwa, na jinsi unavyoweza kufuatilia gharama zinazotokana na usajili wako wa Azure, tembelea [muhtasari wa malipo](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Kutatua matatizo

Q: Nilitembelea anwani ya huduma iliyoorodheshwa, na ninaona ukurasa tupu, ukurasa wa karibu wa karibu, au ukurasa wa kosa.

A: Huduma yako huenda haikuweza kuanzishwa, au inaweza kukosa baadhi ya mipangilio ya usanidi. Ili kuchunguza zaidi:

1. Endesha `azd show`. Bonyeza kiungo chini ya "View in Azure Portal" kufungua kundi la rasilimali katika Azure Portal.
2. Elekea kwenye huduma maalum ya Container App inayoshindwa kupeleka.
3. Bonyeza marekebisho yanayoshindwa chini ya "Revisions with Issues".
4. Pitia "Status details" kwa maelezo zaidi kuhusu aina ya kushindwa.
5. Angalia matokeo ya kumbukumbu kutoka kwa Console log stream na System log stream kutambua makosa yoyote.
6. Ikiwa kumbukumbu zinaandikwa kwenye diski, tumia *Console* katika urambazaji kuungana na shell ndani ya kontena inayotumika.

Kwa maelezo zaidi ya kutatua matatizo, tembelea [Kutatua matatizo ya Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Maelezo ya ziada

Kwa maelezo zaidi kuhusu kuanzisha mradi wako wa `azd`, tembelea [nyaraka zetu rasmi](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Kiarifu cha Kutotegemea**:
Hati hii imetafsiriwa kwa kutumia huduma ya tafsiri ya AI [Co-op Translator](https://github.com/Azure/co-op-translator). Ingawa tunajitahidi kwa usahihi, tafadhali fahamu kuwa tafsiri za kiotomatiki zinaweza kuwa na makosa au upungufu wa usahihi. Hati ya asili katika lugha yake ya asili inapaswa kuzingatiwa kama chanzo cha mamlaka. Kwa taarifa muhimu, tafsiri ya kitaalamu ya binadamu inapendekezwa. Hatubeba dhamana kwa kutoelewana au tafsiri potofu zinazotokana na matumizi ya tafsiri hii.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->