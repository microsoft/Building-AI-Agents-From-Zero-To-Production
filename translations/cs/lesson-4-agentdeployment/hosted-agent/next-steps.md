<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:42:47+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "cs"
}
-->
# Další kroky po `azd init`

## Obsah

1. [Další kroky](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Zprovoznění infrastruktury](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Úprava infrastruktury](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Příprava na produkční provoz](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Fakturace](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Řešení problémů](../../../../lesson-4-agentdeployment/hosted-agent)

## Další kroky

### Zprovoznění infrastruktury a nasazení aplikačního kódu

Spusťte `azd up` pro zprovoznění infrastruktury a nasazení do Azure v jednom kroku (nebo spusťte `azd provision` a poté `azd deploy` pro provedení úkolů samostatně). Navštivte uvedené koncové body služby, abyste viděli svou aplikaci v provozu!

Pro řešení problémů viz [řešení problémů](../../../../lesson-4-agentdeployment/hosted-agent).

### Úprava infrastruktury

Pro popis infrastruktury a aplikace byl přidán soubor `azure.yaml`. Tento soubor obsahuje všechny služby a zdroje, které popisují vaši aplikaci.

Pro přidání nových služeb nebo zdrojů spusťte `azd add`. V případě potřeby můžete také přímo upravit soubor `azure.yaml`.

### Příprava na produkční provoz

Pokud je potřeba, `azd` generuje požadovanou infrastrukturu jako kód v paměti a používá ji. Pokud chcete vidět nebo upravit infrastrukturu, kterou `azd` používá, spusťte `azd infra gen` pro uložení na disk.

Pokud to uděláte, budou vytvořeny některé další adresáře:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Poznámka*: Jakmile infrastrukturu vygenerujete na disk, tyto soubory jsou zdrojem pravdy pro azd. Jakékoliv změny provedené v `azure.yaml` (například pomocí `azd add`) nebudou v infrastruktuře zohledněny, dokud ji znovu nevygenerujete pomocí `azd infra gen`. Před přepsáním souborů budete vyzváni. Můžete použít `--force` k vynucení přepsání souborů bez výzvy.

Nakonec spusťte `azd pipeline config` pro konfiguraci CI/CD nasazovacího pipeline.

## Fakturace

Navštivte stránku *Cost Management + Billing* v Azure Portálu pro sledování aktuálních výdajů. Pro více informací o tom, jak jste fakturováni a jak můžete sledovat náklady vzniklé ve vašich Azure předplatných, navštivte [přehled fakturace](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Řešení problémů

Otázka: Navštívil jsem uvedený koncový bod služby a vidím prázdnou stránku, obecnou uvítací stránku nebo chybovou stránku.

Odpověď: Vaše služba se možná nespustila nebo jí chybí některá konfigurační nastavení. Pro další vyšetření:

1. Spusťte `azd show`. Klikněte na odkaz pod "Zobrazit v Azure Portálu" pro otevření skupiny zdrojů v Azure Portálu.
2. Přejděte ke konkrétní službě Container App, která se nedaří nasadit.
3. Klikněte na neúspěšnou revizi pod "Revize s problémy".
4. Prohlédněte si "Podrobnosti stavu" pro více informací o typu selhání.
5. Sledujte výstupy logů z Console log stream a System log stream pro identifikaci chyb.
6. Pokud jsou logy zapisovány na disk, použijte *Console* v navigaci pro připojení do shellu běžícího kontejneru.

Pro více informací o řešení problémů navštivte [řešení problémů Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Další informace

Pro další informace o nastavení vašeho projektu `azd` navštivte naše oficiální [dokumentace](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Prohlášení o vyloučení odpovědnosti**:  
Tento dokument byl přeložen pomocí AI překladatelské služby [Co-op Translator](https://github.com/Azure/co-op-translator). Přestože usilujeme o přesnost, mějte prosím na paměti, že automatizované překlady mohou obsahovat chyby nebo nepřesnosti. Původní dokument v jeho mateřském jazyce by měl být považován za autoritativní zdroj. Pro důležité informace se doporučuje profesionální lidský překlad. Nejsme odpovědní za jakékoliv nedorozumění nebo nesprávné výklady vyplývající z použití tohoto překladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->