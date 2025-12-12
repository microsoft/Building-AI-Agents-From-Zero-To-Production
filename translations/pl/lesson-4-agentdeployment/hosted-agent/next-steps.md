<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c66e79243b2f1c2bd8ba0105275c427e",
  "translation_date": "2025-12-12T19:34:51+00:00",
  "source_file": "lesson-4-agentdeployment/hosted-agent/next-steps.md",
  "language_code": "pl"
}
-->
# Kolejne kroki po `azd init`

## Spis treści

1. [Kolejne kroki](../../../../lesson-4-agentdeployment/hosted-agent)
   1. [Provisioning infrastruktury](../../../../lesson-4-agentdeployment/hosted-agent)
   2. [Modyfikacja infrastruktury](../../../../lesson-4-agentdeployment/hosted-agent)
   3. [Przygotowanie do produkcji](../../../../lesson-4-agentdeployment/hosted-agent)
2. [Rozliczenia](../../../../lesson-4-agentdeployment/hosted-agent)
3. [Rozwiązywanie problemów](../../../../lesson-4-agentdeployment/hosted-agent)

## Kolejne kroki

### Provisioning infrastruktury i wdrożenie kodu aplikacji

Uruchom `azd up`, aby w jednym kroku przygotować infrastrukturę i wdrożyć aplikację do Azure (lub uruchom `azd provision`, a następnie `azd deploy`, aby wykonać te zadania osobno). Odwiedź wymienione punkty końcowe usług, aby zobaczyć działającą aplikację!

Aby rozwiązać ewentualne problemy, zobacz [rozwiązywanie problemów](../../../../lesson-4-agentdeployment/hosted-agent).

### Modyfikacja infrastruktury

Aby opisać infrastrukturę i aplikację, dodano plik `azure.yaml`. Ten plik zawiera wszystkie usługi i zasoby opisujące Twoją aplikację.

Aby dodać nowe usługi lub zasoby, uruchom `azd add`. Możesz także edytować plik `azure.yaml` bezpośrednio, jeśli zajdzie taka potrzeba.

### Przygotowanie do produkcji

W razie potrzeby `azd` generuje wymaganą infrastrukturę jako kod w pamięci i z niej korzysta. Jeśli chcesz zobaczyć lub zmodyfikować infrastrukturę używaną przez `azd`, uruchom `azd infra gen`, aby zapisać ją na dysku.

Jeśli to zrobisz, zostaną utworzone dodatkowe katalogi:

```yaml
- infra/            # Infrastructure as Code (bicep) files
  - main.bicep      # main deployment module
  - resources.bicep # resources shared across your application's services
  - modules/        # Library modules
```

*Uwaga*: Po wygenerowaniu infrastruktury na dysk, te pliki są źródłem prawdy dla azd. Wszelkie zmiany wprowadzone w `azure.yaml` (np. przez `azd add`) nie będą odzwierciedlone w infrastrukturze, dopóki nie wygenerujesz jej ponownie za pomocą `azd infra gen`. Program zapyta Cię przed nadpisaniem plików. Możesz użyć `--force`, aby wymusić nadpisanie plików bez pytania.

Na koniec uruchom `azd pipeline config`, aby skonfigurować pipeline wdrożeniowy CI/CD.

## Rozliczenia

Odwiedź stronę *Cost Management + Billing* w Azure Portal, aby śledzić bieżące wydatki. Aby uzyskać więcej informacji o tym, jak jesteś rozliczany i jak możesz monitorować koszty ponoszone w subskrypcjach Azure, odwiedź [billing overview](https://learn.microsoft.com/azure/developer/intro/azure-developer-billing).

## Rozwiązywanie problemów

P: Odwiedziłem wymieniony punkt końcowy usługi i widzę pustą stronę, ogólną stronę powitalną lub stronę błędu.

O: Twoja usługa mogła nie uruchomić się poprawnie lub może brakować niektórych ustawień konfiguracyjnych. Aby zbadać problem dalej:

1. Uruchom `azd show`. Kliknij link pod "View in Azure Portal", aby otworzyć grupę zasobów w Azure Portal.
2. Przejdź do konkretnej usługi Container App, która nie udała się wdrożyć.
3. Kliknij na nieudaną rewizję pod "Revisions with Issues".
4. Przejrzyj "Status details", aby uzyskać więcej informacji o rodzaju błędu.
5. Obserwuj wyjścia logów z Console log stream i System log stream, aby zidentyfikować błędy.
6. Jeśli logi są zapisywane na dysku, użyj *Console* w nawigacji, aby połączyć się z powłoką wewnątrz działającego kontenera.

Aby uzyskać więcej informacji o rozwiązywaniu problemów, odwiedź [Container Apps troubleshooting](https://learn.microsoft.com/azure/container-apps/troubleshooting). 

### Dodatkowe informacje

Aby uzyskać dodatkowe informacje o konfiguracji projektu `azd`, odwiedź nasze oficjalne [dokumenty](https://learn.microsoft.com/azure/developer/azure-developer-cli/make-azd-compatible?pivots=azd-convert).

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Zastrzeżenie**:  
Niniejszy dokument został przetłumaczony za pomocą usługi tłumaczenia AI [Co-op Translator](https://github.com/Azure/co-op-translator). Mimo że dokładamy starań, aby tłumaczenie było jak najbardziej precyzyjne, prosimy mieć na uwadze, że automatyczne tłumaczenia mogą zawierać błędy lub nieścisłości. Oryginalny dokument w języku źródłowym powinien być uznawany za źródło autorytatywne. W przypadku informacji krytycznych zalecane jest skorzystanie z profesjonalnego tłumaczenia wykonanego przez człowieka. Nie ponosimy odpowiedzialności za jakiekolwiek nieporozumienia lub błędne interpretacje wynikające z korzystania z tego tłumaczenia.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->