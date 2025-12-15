<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:38:24+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "fi"
}
-->
# Seuraavat vaiheet komennon `azd init` jälkeen

## Sisällysluettelo

1. [Seuraavat vaiheet](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Infrastruktuurin provisiointi](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Infrastruktuurin muokkaaminen](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Tuotantovalmiiksi pääseminen](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Laskutus](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Vianmääritys](../../../../lesson-4-agentdeployment/hosted-agent)

## Seuraavat vaiheet

### Infrastruktuurin provisiointi ja sovelluskoodin käyttöönotto

Suorita `azd up` provisioidaksesi infrastruktuurin ja ottaaksesi sovelluksen käyttöön Azureen yhdellä komennolla (tai suorita ensin `azd provision` ja sitten `azd deploy` tehtävien erilliseen suorittamiseen). Käy luetelluissa palvelupisteissä nähdäksesi sovelluksesi toiminnassa!

Jos kohtaat ongelmia, katso [vianmääritys](../../../../lesson-4-agentdeployment/hosted-agent).

### Infrastruktuurin muokkaaminen

Infrastruktuurin ja sovelluksen kuvaamiseksi lisättiin tiedosto `azure.yaml`. Tämä tiedosto sisältää kaikki palvelut ja resurssit, jotka kuvaavat sovellustasi.

Lisätäksesi uusia palveluita tai resursseja, suorita `azd add`. Voit myös tarvittaessa muokata tiedostoa `azure.yaml` suoraan.

### Tuotantovalmiiksi pääseminen

Tarvittaessa `azd` generoi vaaditun infrastruktuurin koodina muistissa ja käyttää sitä. Jos haluat nähdä tai muokata `azd`:n käyttämää infrastruktuuria, suorita `azd infra gen` tallentaaksesi sen levylle.

Jos teet tämän, luodaan joitakin lisähakemistoja:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Huom*: Kun olet generoinut infrastruktuurin levylle, nämä tiedostot ovat `azd`:n totuuden lähde. Kaikki `azure.yaml`-tiedostoon tehdyt muutokset (esim. `azd add` -komennolla) eivät näy infrastruktuurissa ennen kuin generoit sen uudelleen komennolla `azd infra gen`. Komento kysyy vahvistusta ennen tiedostojen ylikirjoittamista. Voit käyttää `--force`-valitsinta pakottaaksesi `azd infra gen` -komennon ylikirjoittamaan tiedostot ilman vahvistusta.

Lopuksi suorita `azd pipeline config` konfiguroidaksesi CI/CD-julkaisuputken.

## Laskutus

Käy *Cost Management + Billing* -sivulla Azure-portaalissa seurataksesi nykyisiä kuluja. Lisätietoja laskutuksesta ja siitä, miten voit seurata Azure-tilauksissasi syntyviä kustannuksia, löydät osoitteesta [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Vianmääritys

K: Kävin luetellussa palvelupisteessä, ja näen tyhjän sivun, yleisen tervetulossivun tai virhesivun.

V: Palvelusi ei ehkä käynnistynyt oikein tai siltä puuttuu joitakin konfiguraatioasetuksia. Tutkiaksesi asiaa tarkemmin:

1. Suorita `azd show`. Klikkaa linkkiä "View in Azure Portal" avataksesi resurssiryhmän Azure-portaalissa.
2. Siirry siihen Container App -palveluun, jonka käyttöönotto epäonnistuu.
3. Klikkaa epäonnistuvaa revisiota kohdassa "Revisions with Issues".
4. Tarkastele "Status details" saadaksesi lisätietoja virheen tyypistä.
5. Tarkkaile konsolin lokivirtoja ja järjestelmän lokivirtoja virheiden tunnistamiseksi.
6. Jos lokit kirjoitetaan levylle, käytä *Console*-näkymää yhdistääksesi ajossa olevaan konttiin komentoriville.

Lisätietoja vianmäärityksestä löydät osoitteesta [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Lisätietoja

Lisätietoja `azd`-projektisi perustamisesta löydät virallisista [dokumenteistamme](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vastuuvapauslauseke**:
Tämä asiakirja on käännetty käyttämällä tekoälypohjaista käännöspalvelua [Co-op Translator](https://github.com/Azure/co-op-translator). Vaikka pyrimme tarkkuuteen, otathan huomioon, että automaattikäännöksissä saattaa esiintyä virheitä tai epätarkkuuksia. Alkuperäistä asiakirjaa sen alkuperäiskielellä tulee pitää virallisena lähteenä. Tärkeissä tiedoissa suositellaan ammattimaista ihmiskäännöstä. Emme ole vastuussa tämän käännöksen käytöstä aiheutuvista väärinymmärryksistä tai tulkinnoista.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->