# Lektion 2 Agentudvikling

Velkommen til anden lektion af kurset "Bygning af AI-agent fra nul til produktion"!

I denne lektion vil vi dække:

- Værktøjerne til at skabe vores AI-agenter
  
- Opsætningsinstruktioner for vores udviklingsressourcer

- Bedste praksis for AI-agentudvikling
  
- Gennemgang af kode til oprettelse af vores AI-agenter
  
Lad os starte med at se på de værktøjer, vi vil bruge til at skabe vores AI-agenter.

## Værktøjer og opsætningsinstruktioner

### Microsoft Foundry

For adgang til store sprogmodeller (LLMs) vil vi bruge [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry). Der er omkostninger forbundet med brug af Foundry, så sørg venligst for at følge instruktionerne for kontoopsætning, hvis du ikke allerede har adgang.

### OpenAI-modeller

Agentens kodeeksempler i dette kursus er sat op til at bruge OpenAI-modeller gennem [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry).

Brug denne vejledning til at lære, hvordan man deployerer en model vha. Foundry: [Deploy Microsoft Foundry Models in the Foundry portal](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models?view=foundry-classic)

Vælg en GPT-5 serie model (for eksempel `gpt-5.1`) til dette kursus. Undgå pensionerede modeller som GPT-4o og GPT-4.1, der når end-of-life i 2026.

### Microsoft Agent Framework

Som nævnt tidligere vil vi bruge [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) til både at skabe og orkestrere vores AI-agenter.

Du skal bruge **Python 3.12 eller nyere**. For at installere Microsoft Agent Framework og andre nødvendige pakker, kør følgende kommando i projektets rodmappe:

```bash
pip install -r requirements.txt
```

### Autentificer med Azure

Agenterne autentificerer til Microsoft Foundry ved hjælp af dine Azure CLI-legitimationsoplysninger
(`AzureCliCredential`), så du skal logge ind, inden du kører nogen prøvekode:

```bash
az login
# Hvis du har mere end ét abonnement, skal du vælge det med dit Foundry-projekt:
az account set --subscription "<your-subscription-id>"
```

Sørg for, at din konto har rollen **Azure AI User** (eller tilsvarende) på Foundry
projektet, så den kan kalde model- og agent-API'erne.

### Opsætning af .env-variabler

For at køre kodeeksemplerne i dette kursus, skal du oprette en `.env`-fil i projektets rodmappe.

For at gøre det nemmere kan du kopiere den medfølgende `.env.example`-fil:

```bash
cp .env.example .env
``` 

Udfyld herefter de to variabler, som agenterne læser ( `FoundryChatClient` henter dem
automatisk):

| Variabel | Hvad det er | Hvor du finder det |
|----------|-------------|-------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Din Foundry **projekt** endpoint, der slutter med `/api/projects/<project>` | Foundry portalen → dit projekt → **Oversigt** → *Endpoints* |
| `FOUNDRY_MODEL` | Navnet på modeludrulningen, som dine agenter kører på (for eksempel `gpt-5.1`) | Foundry portalen → **Modeller + endpoints** |

### Opret employee vector store

Et eksempel — **Employee Search Agent** — søger i et medarbejderkatalog gemt i en
Microsoft Foundry **vector store**. Opret den én gang, og kopier ID'et, den udskriver, ind i din `.env`
som `VECTOR_STORE_ID` (kør fra repository-roden, så den henter din `.env`):

```bash
python lesson-2-agent-development/setup_vector_store.py
```

### Kør et eksempel

Hver agent kører sin egen lokale DevUI. For eksempel:

```bash
python lesson-2-agent-development/employee-search-agent.py
```

Åbn derefter den udskrevne URL `http://localhost:<port>` i din browser for at chatte med agenten.

## Agenterne i denne lektion

Hvert eksempel er en selvstændig agent bygget med Microsoft Agent Framework. Sammen
implementerer de de scenarier, du designede i [Lektion 1](../lesson-1-agent-design/README.md):

| Eksempel | Lektion 1 scenario | Brugt værktøj | Port |
|----------|-------------------|--------------|------|
| `employee-search-agent.py` | Scenario 1 — Medarbejdersøgning | Foundry-hosted **fil-søgning** over en vector store | 8090 |
| `task-recommendation-agent.py` | Scenario 2 — Opgaveanbefaling | **GitHub MCP** server (hostet MCP-værktøj) | 8095 |
| `azure-learning-agent.py` | Scenario 3 — Kodeassistent (research) | **Microsoft Learn MCP** server (hostet MCP-værktøj) | 8092 |
| `coding-agent.py` | Scenario 3 — Kodeassistent (kode) | **Code Interpreter** | 8093 |
| `learning-recommendation-agent.py` | Støtteagent | Learn MCP + ræsonnering | 8091 |
| `agent-orchestration.py` | Binder scenarierne sammen | Multi-agent **handoff** orkestrering | 8094 |

> **Bemærk om Task Recommendation Agent.** `task-recommendation-agent.py` kræver en
> `GITHUB_PERSONAL_ACCESS_TOKEN` i din `.env` (opret en ved
> <https://github.com/settings/personal-access-tokens/new>). Den læser en udviklers seneste
> GitHub-aktivitet og anbefaler 1–3 åbne issues, der matcher — præcis som Scenario 2 designet.
> Dette er det eneste eksempel, der kalder GitHub; de andre kræver kun dit Foundry-projekt.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Ansvarsfraskrivelse**:
Dette dokument er blevet oversat ved hjælp af AI-oversættelsestjenesten [Co-op Translator](https://github.com/Azure/co-op-translator). Selvom vi bestræber os på nøjagtighed, skal du være opmærksom på, at automatiserede oversættelser kan indeholde fejl eller unøjagtigheder. Det originale dokument på dets oprindelige sprog bør betragtes som den autoritative kilde. For kritisk information anbefales professionel menneskelig oversættelse. Vi påtager os intet ansvar for misforståelser eller fejltolkninger, der opstår som følge af brugen af denne oversættelse.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->