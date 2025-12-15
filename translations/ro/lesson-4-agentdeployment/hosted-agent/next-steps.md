<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:43:44+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "ro"
}
-->
# Pașii următori după `azd init`

## Cuprins

1. [Pașii următori](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisionarea infrastructurii](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modificarea infrastructurii](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Pregătirea pentru producție](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Facturare](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Depanare](../../../../lesson-4-agentdeployment/hosted-agent)

## Pașii următori

### Provisionarea infrastructurii și implementarea codului aplicației

Rulați `azd up` pentru a provisiona infrastructura și a implementa în Azure într-un singur pas (sau rulați `azd provision` apoi `azd deploy` pentru a realiza sarcinile separat). Vizitați punctele finale ale serviciului listate pentru a vedea aplicația dvs. funcționând!

Pentru depanarea oricăror probleme, consultați [depanarea](../../../../lesson-4-agentdeployment/hosted-agent).

### Modificarea infrastructurii

Pentru a descrie infrastructura și aplicația, a fost adăugat fișierul `azure.yaml`. Acest fișier conține toate serviciile și resursele care descriu aplicația dvs.

Pentru a adăuga servicii sau resurse noi, rulați `azd add`. De asemenea, puteți edita direct fișierul `azure.yaml` dacă este necesar.

### Pregătirea pentru producție

Când este necesar, `azd` generează infrastructura necesară ca cod în memorie și o folosește. Dacă doriți să vedeți sau să modificați infrastructura pe care o folosește `azd`, rulați `azd infra gen` pentru a o salva pe disc.

Dacă faceți acest lucru, vor fi create câteva directoare suplimentare:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Notă*: Odată ce ați generat infrastructura pe disc, acele fișiere devin sursa de adevăr pentru azd. Orice modificări făcute în `azure.yaml` (cum ar fi prin `azd add`) nu vor fi reflectate în infrastructură până când nu o regenerați din nou cu `azd infra gen`. Veți fi întrebat înainte de a suprascrie fișierele. Puteți folosi `--force` pentru a forța `azd infra gen` să suprascrie fișierele fără a cere confirmare.

În final, rulați `azd pipeline config` pentru a configura un pipeline de implementare CI/CD.

## Facturare

Vizitați pagina *Cost Management + Billing* din Azure Portal pentru a urmări cheltuielile curente. Pentru mai multe informații despre modul în care sunteți facturat și cum puteți monitoriza costurile generate în abonamentele dvs. Azure, vizitați [prezentarea facturării](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Depanare

Î: Am vizitat punctul final al serviciului listat și văd o pagină goală, o pagină generică de bun venit sau o pagină de eroare.

R: Serviciul dvs. poate să nu fi pornit sau poate lipsi unele setări de configurare. Pentru a investiga mai departe:

1. Rulați `azd show`. Faceți clic pe linkul de sub "View in Azure Portal" pentru a deschide grupul de resurse în Azure Portal.
2. Navigați la serviciul specific Container App care nu reușește să se implementeze.
3. Faceți clic pe revizia care eșuează sub "Revisions with Issues".
4. Examinați "Status details" pentru mai multe informații despre tipul de eșec.
5. Observați ieșirile din loguri din Console log stream și System log stream pentru a identifica eventualele erori.
6. Dacă logurile sunt scrise pe disc, folosiți *Console* din navigație pentru a vă conecta la un shell în containerul care rulează.

Pentru mai multe informații de depanare, vizitați [Depanarea Container Apps](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Informații suplimentare

Pentru informații suplimentare despre configurarea proiectului dvs. `azd`, vizitați documentația noastră oficială [docs](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Declinare de responsabilitate**:  
Acest document a fost tradus folosind serviciul de traducere AI [Co-op Translator](https://github.com/Azure/co-op-translator). Deși ne străduim pentru acuratețe, vă rugăm să rețineți că traducerile automate pot conține erori sau inexactități. Documentul original în limba sa nativă trebuie considerat sursa autorizată. Pentru informații critice, se recomandă traducerea profesională realizată de un specialist uman. Nu ne asumăm răspunderea pentru eventualele neînțelegeri sau interpretări greșite rezultate din utilizarea acestei traduceri.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->