<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:42:11+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "hu"
}
-->
# Következő lépések az `azd init` után

## Tartalomjegyzék

1. [Következő lépések](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Infrastruktúra előkészítése](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Infrastruktúra módosítása](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Előkészület a termelési környezetre](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Számlázás](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Hibaelhárítás](../../../../lesson-4-agentdeployment/hosted-agent)

## Következő lépések

### Infrastruktúra előkészítése és alkalmazáskód telepítése

Futtassa az `azd up` parancsot az infrastruktúra előkészítéséhez és az Azure-ba történő telepítéshez egy lépésben (vagy futtassa külön-külön az `azd provision` majd az `azd deploy` parancsokat). Látogassa meg a felsorolt szolgáltatás végpontokat, hogy lássa az alkalmazását működés közben!

A problémák elhárításához lásd a [hibaelhárítás](../../../../lesson-4-agentdeployment/hosted-agent) részt.

### Infrastruktúra módosítása

Az infrastruktúra és az alkalmazás leírásához hozzá lett adva az `azure.yaml` fájl. Ez a fájl tartalmazza az összes szolgáltatást és erőforrást, amelyek leírják az alkalmazását.

Új szolgáltatások vagy erőforrások hozzáadásához futtassa az `azd add` parancsot. Szükség esetén közvetlenül is szerkesztheti az `azure.yaml` fájlt.

### Előkészület a termelési környezetre

Ha szükséges, az `azd` a memóriában generálja a szükséges infrastruktúrát kódként, és azt használja. Ha meg szeretné tekinteni vagy módosítani az `azd` által használt infrastruktúrát, futtassa az `azd infra gen` parancsot, hogy azt lemezre mentse.

Ha ezt megteszi, néhány további könyvtár jön létre:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Megjegyzés*: Miután az infrastruktúrát lemezre generálta, ezek a fájlok lesznek az `azd` számára az igazság forrásai. Az `azure.yaml` fájlban végrehajtott bármilyen változtatás (például az `azd add` használatával) nem fog megjelenni az infrastruktúrában, amíg újra nem generálja azt az `azd infra gen` paranccsal. A fájlok felülírása előtt megerősítést kér. A `--force` kapcsolóval kényszerítheti az `azd infra gen` parancsot, hogy megerősítés nélkül felülírja a fájlokat.

Végül futtassa az `azd pipeline config` parancsot egy CI/CD telepítési pipeline konfigurálásához.

## Számlázás

Látogassa meg az *Költségkezelés + Számlázás* oldalt az Azure Portalon a jelenlegi kiadások nyomon követéséhez. További információkért arról, hogyan történik a számlázás, és hogyan figyelheti az Azure-előfizetéseiben felmerülő költségeket, látogassa meg a [számlázási áttekintő](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing) oldalt.

## Hibaelhárítás

K: Meglátogattam a felsorolt szolgáltatás végpontot, és üres oldalt, általános üdvözlő oldalt vagy hibás oldalt látok.

V: Lehet, hogy a szolgáltatás nem indult el, vagy hiányoznak bizonyos konfigurációs beállítások. A további vizsgálathoz:

1. Futtassa az `azd show` parancsot. Kattintson a "Megtekintés az Azure Portalon" alatti hivatkozásra, hogy megnyissa az erőforráscsoportot az Azure Portalon.
2. Navigáljon a konkrét, telepítéskor hibát okozó Container App szolgáltatáshoz.
3. Kattintson a "Problémás verziók" alatt a hibás verzióra.
4. Tekintse át az "Állapot részletei" részt a hiba típusának további információiért.
5. Figyelje meg a Konzol naplófolyam és a Rendszer naplófolyam kimeneteit a hibák azonosításához.
6. Ha a naplók lemezre íródnak, használja a navigációban a *Konzol* opciót, hogy csatlakozzon egy shellhez a futó konténerben.

További hibaelhárítási információkért látogassa meg a [Container Apps hibaelhárítás](https://learn.microsoft.com/azure/container-apps/troubleshooting) oldalt.

### További információk

Az `azd` projekt beállításával kapcsolatos további információkért látogassa meg hivatalos [dokumentációnkat](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Jogi nyilatkozat**:
Ezt a dokumentumot az AI fordító szolgáltatás, a [Co-op Translator](https://github.com/Azure/co-op-translator) segítségével fordítottuk le. Bár a pontosságra törekszünk, kérjük, vegye figyelembe, hogy az automatikus fordítások hibákat vagy pontatlanságokat tartalmazhatnak. Az eredeti dokumentum az anyanyelvén tekintendő hiteles forrásnak. Fontos információk esetén professzionális emberi fordítást javaslunk. Nem vállalunk felelősséget a fordítás használatából eredő félreértésekért vagy félreértelmezésekért.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->