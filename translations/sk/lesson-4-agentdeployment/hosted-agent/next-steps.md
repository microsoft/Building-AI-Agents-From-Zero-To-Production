<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:43:16+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "sk"
}
-->
# Ďalšie kroky po `azd init`

## Obsah

1. [Ďalšie kroky](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Zabezpečenie infraštruktúry](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Úprava infraštruktúry](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Príprava na produkciu](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fakturácia](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Riešenie problémov](../../../../lesson-4-agentdeployment/hosted-agent)

## Ďalšie kroky

### Zabezpečenie infraštruktúry a nasadenie aplikačného kódu

Spustite `azd up` na zabezpečenie infraštruktúry a nasadenie do Azure v jednom kroku (alebo spustite `azd provision` a potom `azd deploy` na vykonanie úloh samostatne). Navštívte uvedené koncové body služby, aby ste videli svoju aplikáciu v prevádzke!

Ak chcete vyriešiť akékoľvek problémy, pozrite si [riešenie problémov](../../../../lesson-4-agentdeployment/hosted-agent).

### Úprava infraštruktúry

Na popis infraštruktúry a aplikácie bol pridaný súbor `azure.yaml`. Tento súbor obsahuje všetky služby a zdroje, ktoré popisujú vašu aplikáciu.

Ak chcete pridať nové služby alebo zdroje, spustite `azd add`. Môžete tiež priamo upraviť súbor `azure.yaml`, ak je to potrebné.

### Príprava na produkciu

Keď je to potrebné, `azd` generuje požadovanú infraštruktúru ako kód v pamäti a používa ju. Ak chcete vidieť alebo upraviť infraštruktúru, ktorú `azd` používa, spustite `azd infra gen` na jej uloženie na disk.

Ak to urobíte, vytvoria sa niektoré ďalšie adresáre:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Poznámka*: Akonáhle infraštruktúru vygenerujete na disk, tieto súbory sú zdrojom pravdy pre azd. Akékoľvek zmeny vykonané v `azure.yaml` (napríklad cez `azd add`) sa v infraštruktúre neprejavia, kým ju znova nevygenerujete pomocou `azd infra gen`. Pred prepísaním súborov vás to upozorní. Môžete použiť `--force` na vynútenie prepísania súborov bez upozornenia.

Nakoniec spustite `azd pipeline config` na konfiguráciu CI/CD nasadzovacieho pipeline.

## Fakturácia

Navštívte stránku *Cost Management + Billing* v Azure Portáli, aby ste sledovali aktuálne výdavky. Pre viac informácií o tom, ako ste fakturovaní a ako môžete monitorovať náklady vzniknuté vo vašich Azure predplatných, navštívte [prehľad fakturácie](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Riešenie problémov

Otázka: Navštívil som uvedený koncový bod služby a vidím prázdnu stránku, všeobecnú uvítaciu stránku alebo chybovú stránku.

Odpoveď: Vaša služba sa mohla nepodarilo spustiť alebo jej môžu chýbať niektoré konfiguračné nastavenia. Pre ďalšie vyšetrovanie:

1. Spustite `azd show`. Kliknite na odkaz pod "View in Azure Portal" pre otvorenie skupiny zdrojov v Azure Portáli.
2. Prejdite na konkrétnu službu Container App, ktorá sa nepodarilo nasadiť.
3. Kliknite na neúspešnú revíziu pod "Revisions with Issues".
4. Skontrolujte "Status details" pre viac informácií o type zlyhania.
5. Sledujte výstupy logov z Console log stream a System log stream, aby ste identifikovali chyby.
6. Ak sa logy zapisujú na disk, použite *Console* v navigácii na pripojenie k shellu v bežiacom kontejnery.

Pre viac informácií o riešení problémov navštívte [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Ďalšie informácie

Pre ďalšie informácie o nastavení vášho projektu `azd` navštívte naše oficiálne [dokumenty](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zrieknutie sa zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Aj keď sa snažíme o presnosť, majte prosím na pamäti, že automatizované preklady môžu obsahovať chyby alebo nepresnosti. Originálny dokument v jeho pôvodnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za akékoľvek nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->