<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:25:57+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "de"
}
-->
# Nächste Schritte nach `azd init`

## Inhaltsverzeichnis

1. [Nächste Schritte](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Infrastruktur bereitstellen](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Infrastruktur ändern](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Produktionsreife erreichen](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Abrechnung](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Fehlerbehebung](../../../../lesson-4-agentdeployment/hosted-agent)

## Nächste Schritte

### Infrastruktur bereitstellen und Anwendungscode bereitstellen

Führen Sie `azd up` aus, um Ihre Infrastruktur bereitzustellen und in einem Schritt auf Azure bereitzustellen (oder führen Sie `azd provision` und dann `azd deploy` aus, um die Aufgaben separat auszuführen). Besuchen Sie die aufgeführten Service-Endpunkte, um Ihre Anwendung in Betrieb zu sehen!

Um Probleme zu beheben, siehe [Fehlerbehebung](../../../../lesson-4-agentdeployment/hosted-agent).

### Infrastruktur ändern

Um die Infrastruktur und Anwendung zu beschreiben, wurde `azure.yaml` hinzugefügt. Diese Datei enthält alle Dienste und Ressourcen, die Ihre Anwendung beschreiben.

Um neue Dienste oder Ressourcen hinzuzufügen, führen Sie `azd add` aus. Sie können die Datei `azure.yaml` bei Bedarf auch direkt bearbeiten.

### Produktionsreife erreichen

Wenn nötig, generiert `azd` die erforderliche Infrastruktur als Code im Speicher und verwendet sie. Wenn Sie die Infrastruktur, die `azd` verwendet, sehen oder ändern möchten, führen Sie `azd infra gen` aus, um sie auf der Festplatte zu speichern.

Wenn Sie dies tun, werden einige zusätzliche Verzeichnisse erstellt:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Hinweis*: Sobald Sie Ihre Infrastruktur auf der Festplatte generiert haben, sind diese Dateien die Quelle der Wahrheit für azd. Änderungen an `azure.yaml` (z. B. durch `azd add`) werden in der Infrastruktur nicht reflektiert, bis Sie sie mit `azd infra gen` erneut generieren. Es wird Sie vor dem Überschreiben der Dateien auffordern. Sie können `--force` übergeben, um `azd infra gen` zu zwingen, die Dateien ohne Aufforderung zu überschreiben.

Führen Sie abschließend `azd pipeline config` aus, um eine CI/CD-Bereitstellungspipeline zu konfigurieren.

## Abrechnung

Besuchen Sie die Seite *Kostenverwaltung + Abrechnung* im Azure-Portal, um die aktuellen Ausgaben zu verfolgen. Für weitere Informationen darüber, wie Sie abgerechnet werden und wie Sie die in Ihren Azure-Abonnements anfallenden Kosten überwachen können, besuchen Sie [Abrechnungsübersicht](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Fehlerbehebung

F: Ich habe den aufgeführten Service-Endpunkt besucht und sehe eine leere Seite, eine generische Willkommensseite oder eine Fehlerseite.

A: Ihr Dienst konnte möglicherweise nicht gestartet werden oder es fehlen einige Konfigurationseinstellungen. Um weiter zu untersuchen:

1. Führen Sie `azd show` aus. Klicken Sie auf den Link unter "View in Azure Portal", um die Ressourcengruppe im Azure-Portal zu öffnen.
2. Navigieren Sie zum spezifischen Container-App-Dienst, der nicht bereitgestellt wird.
3. Klicken Sie auf die fehlerhafte Revision unter "Revisions with Issues".
4. Überprüfen Sie die "Statusdetails" für weitere Informationen zur Art des Fehlers.
5. Beobachten Sie die Protokollausgaben aus der Konsolen-Protokollstream und System-Protokollstream, um Fehler zu identifizieren.
6. Wenn Protokolle auf die Festplatte geschrieben werden, verwenden Sie *Console* in der Navigation, um eine Shell innerhalb des laufenden Containers zu verbinden.

Für weitere Informationen zur Fehlerbehebung besuchen Sie [Container Apps Fehlerbehebung](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Zusätzliche Informationen

Für weitere Informationen zur Einrichtung Ihres `azd`-Projekts besuchen Sie unsere offiziellen [Dokumentationen](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Haftungsausschluss**:  
Dieses Dokument wurde mit dem KI-Übersetzungsdienst [Co-op Translator](https://github.com/Azure/co-op-translator) übersetzt. Obwohl wir uns um Genauigkeit bemühen, beachten Sie bitte, dass automatisierte Übersetzungen Fehler oder Ungenauigkeiten enthalten können. Das Originaldokument in seiner Ursprungssprache gilt als maßgebliche Quelle. Für wichtige Informationen wird eine professionelle menschliche Übersetzung empfohlen. Wir übernehmen keine Haftung für Missverständnisse oder Fehlinterpretationen, die aus der Nutzung dieser Übersetzung entstehen.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->