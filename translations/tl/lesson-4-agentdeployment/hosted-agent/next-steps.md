<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:41:06+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "tl"
}
-->
# Mga Susunod na Hakbang pagkatapos ng `azd init`

## Talaan ng Nilalaman

1. [Mga Susunod na Hakbang](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Mag-provision ng imprastruktura](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Baguhin ang imprastruktura](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Paghahanda para sa produksyon](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Pagbabayad](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Pag-troubleshoot](../../../../lesson-4-agentdeployment/hosted-agent)

## Mga Susunod na Hakbang

### Mag-provision ng imprastruktura at i-deploy ang application code

Patakbuhin ang `azd up` upang mag-provision ng iyong imprastruktura at i-deploy sa Azure sa isang hakbang (o patakbuhin ang `azd provision` pagkatapos ay `azd deploy` upang gawin ang mga gawain nang hiwalay). Bisitahin ang mga service endpoint na nakalista upang makita ang iyong application na tumatakbo!

Para mag-troubleshoot ng anumang isyu, tingnan ang [pag-troubleshoot](../../../../lesson-4-agentdeployment/hosted-agent).

### Baguhin ang imprastruktura

Upang ilarawan ang imprastruktura at application, idinagdag ang `azure.yaml`. Ang file na ito ay naglalaman ng lahat ng serbisyo at resources na naglalarawan ng iyong application.

Upang magdagdag ng mga bagong serbisyo o resources, patakbuhin ang `azd add`. Maaari mo ring direktang i-edit ang `azure.yaml` na file kung kinakailangan.

### Paghahanda para sa produksyon

Kapag kinakailangan, ang `azd` ay bumubuo ng kinakailangang imprastruktura bilang code sa memorya at ginagamit ito. Kung nais mong makita o baguhin ang imprastruktura na ginagamit ng `azd`, patakbuhin ang `azd infra gen` upang i-save ito sa disk.

Kung gagawin mo ito, ilang karagdagang direktoryo ang malilikha:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Tandaan*: Kapag na-generate mo na ang iyong imprastruktura sa disk, ang mga file na iyon ang magiging source of truth para sa azd. Anumang pagbabago sa `azure.yaml` (tulad ng sa pamamagitan ng `azd add`) ay hindi makikita sa imprastruktura hanggang sa muling i-generate ito gamit ang `azd infra gen`. Hihilingin ka nito bago i-overwrite ang mga file. Maaari mong gamitin ang `--force` upang pilitin ang `azd infra gen` na i-overwrite ang mga file nang hindi nagtatanong.

Sa wakas, patakbuhin ang `azd pipeline config` upang i-configure ang isang CI/CD deployment pipeline.

## Pagbabayad

Bisitahin ang pahina ng *Cost Management + Billing* sa Azure Portal upang subaybayan ang kasalukuyang gastusin. Para sa karagdagang impormasyon tungkol sa kung paano ka sinisingil, at kung paano mo masusubaybayan ang mga nagastos sa iyong mga Azure subscription, bisitahin ang [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Pag-troubleshoot

Q: Binisita ko ang service endpoint na nakalista, at nakikita ko ang isang blangkong pahina, isang pangkalahatang pahina ng welcome, o isang pahina ng error.

A: Maaaring nabigo ang iyong serbisyo na magsimula, o maaaring kulang ito sa ilang mga setting ng configuration. Upang mag-imbestiga pa:

1. Patakbuhin ang `azd show`. I-click ang link sa ilalim ng "View in Azure Portal" upang buksan ang resource group sa Azure Portal.
2. Mag-navigate sa partikular na Container App service na nabibigo sa pag-deploy.
3. I-click ang nabigong revision sa ilalim ng "Revisions with Issues".
4. Suriin ang "Status details" para sa karagdagang impormasyon tungkol sa uri ng pagkabigo.
5. Obserbahan ang mga log output mula sa Console log stream at System log stream upang matukoy ang anumang mga error.
6. Kung ang mga log ay naisulat sa disk, gamitin ang *Console* sa navigation upang kumonekta sa isang shell sa loob ng tumatakbong container.

Para sa karagdagang impormasyon sa pag-troubleshoot, bisitahin ang [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Karagdagang impormasyon

Para sa karagdagang impormasyon tungkol sa pagsasaayos ng iyong `azd` na proyekto, bisitahin ang aming opisyal na [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Paunawa**:  
Ang dokumentong ito ay isinalin gamit ang AI translation service na [Co-op Translator](https://github.com/Azure/co-op-translator). Bagamat nagsusumikap kami para sa katumpakan, pakatandaan na ang mga awtomatikong pagsasalin ay maaaring maglaman ng mga pagkakamali o di-tumpak na impormasyon. Ang orihinal na dokumento sa orihinal nitong wika ang dapat ituring na pangunahing sanggunian. Para sa mahahalagang impormasyon, inirerekomenda ang propesyonal na pagsasalin ng tao. Hindi kami mananagot sa anumang hindi pagkakaunawaan o maling interpretasyon na maaaring magmula sa paggamit ng pagsasaling ito.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->