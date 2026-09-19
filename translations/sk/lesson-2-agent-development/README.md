# Lekcia 2 Vývoj agenta

Vitajte v druhej lekcii kurzu „Budovanie AI agenta od nuly po produkciu“!

V tejto lekcii prejdeme:

- Nástroje na tvorbu našich AI agentov
  
- Inštrukcie na nastavenie našich vývojových zdrojov

- Najlepšie postupy pri vývoji AI agentov
  
- Prechádzka kódom pri vytváraní našich AI agentov
  
Začnime pohľadom na nástroje, ktoré použijeme na vytvorenie našich AI agentov.

## Nástroje a inštrukcie na nastavenie

### Microsoft Foundry

Pre prístup k Veľkým jazykovým modelom (LLM) budeme používať [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry). Používanie Foundry je spojené s nákladmi, preto sa uistite, že postupujete podľa inštrukcií na nastavenie účtu, ak ešte nemáte prístup.

### OpenAI modely

Ukážky kódu agentov v tomto kurze sú nastavené na používanie OpenAI modelov cez [Microsoft Foundry](https://azure.microsoft.com/products/ai-foundry).

Použite tento návod na naučenie sa, ako nasadiť model pomocou Foundry: [Nasadenie modelov Microsoft Foundry v portáli Foundry](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/deploy-foundry-models?view=foundry-classic)

Vyberte si jeden model série GPT-5 (napríklad `gpt-5.1`) pre tento kurz. Vyhnite sa vyradeným modelom, ako sú GPT-4o a GPT-4.1, ktoré končia životnosť v roku 2026.

### Microsoft Agent Framework

Ako bolo spomenuté skôr, budeme používať [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) na vytváranie a orchestráciu našich AI agentov.

Budete potrebovať **Python 3.12 alebo novší**. Na inštaláciu Microsoft Agent Framework a ďalších potrebných balíčkov spustite nasledujúci príkaz v koreňovom adresári tohto projektu:

```bash
pip install -r requirements.txt
```

### Overenie identity s Azure

Agenti sa overujú v Microsoft Foundry pomocou vašich Azure CLI poverení
(`AzureCliCredential`), preto sa musíte prihlásiť pred spustením ľubovoľnej ukážky:

```bash
az login
# Ak máte viac ako jedno predplatné, vyberte to, ktoré obsahuje váš projekt Foundry:
az account set --subscription "<your-subscription-id>"
```

Uistite sa, že váš účet má rolu **Azure AI User** (alebo ekvivalentnú) v projekte Foundry,
aby mohol volať API modelov a agentov.

### Nastavenie premenných v .env

Na spustenie ukážok kódu v tomto kurze budete potrebovať vytvoriť súbor `.env` v koreňovom adresári tohto projektu.

Pre ľahšie nastavenie môžete skopírovať poskytnutý súbor `.env.example`:

```bash
cp .env.example .env
``` 

Potom vyplňte dve premenné, ktoré agenti čítajú (klient `FoundryChatClient` ich
automaticky zachytáva):

| Premenná | Čo to je | Kde ju nájsť |
|----------|------------|------------------|
| `FOUNDRY_PROJECT_ENDPOINT` | Endpoint vášho Foundry **projektu**, končiaci `/api/projects/<project>` | Portal Foundry → váš projekt → **Prehľad** → *Endpointy* |
| `FOUNDRY_MODEL` | Názov nasadeného modelu, na ktorom agenti bežia (napríklad `gpt-5.1`) | Portal Foundry → **Modely + endpointy** |

### Vytvorenie vektorového úložiska pre zamestnancov

Jedna ukážka — **Employee Search Agent** — vyhľadáva v adresári zamestnancov vedenom v
Microsoft Foundry **vektorovom úložisku**. Vytvorte ho raz a skopírujte ID, ktoré vytlačí, do vášho `.env`
ako `VECTOR_STORE_ID` (spustite z koreňa repozitára, aby načítal váš `.env`):

```bash
python lesson-2-agent-development/setup_vector_store.py
```

### Spustenie ukážky

Každý agent spúšťa svoje vlastné lokálne DevUI. Napríklad:

```bash
python lesson-2-agent-development/employee-search-agent.py
```

Potom otvorte vytlačenú URL `http://localhost:<port>` vo vašom prehliadači a komunikujte s agentom.

## Agenti v tejto lekcii

Každá ukážka je samostatný agent vytvorený s Microsoft Agent Framework. Spoločne
implementujú scenáre, ktoré ste navrhli v [Lekcii 1](../lesson-1-agent-design/README.md):

| Ukážka | Scenár z Lekcie 1 | Použitý nástroj | Port |
|--------|-------------------|-----------|------|
| `employee-search-agent.py` | Scenár 1 — Vyhľadávanie zamestnancov | Foundry hosťované **hľadanie súborov** cez vektorové úložisko | 8090 |
| `task-recommendation-agent.py` | Scenár 2 — Odporúčanie úloh | **GitHub MCP** server (hosťovaný MCP nástroj) | 8095 |
| `azure-learning-agent.py` | Scenár 3 — Asistent kódu (výskum) | **Microsoft Learn MCP** server (hosťovaný MCP nástroj) | 8092 |
| `coding-agent.py` | Scenár 3 — Asistent kódu (kódovanie) | **Kódový interpret** | 8093 |
| `learning-recommendation-agent.py` | Podporný agent | Learn MCP + uvažovanie | 8091 |
| `agent-orchestration.py` | Spája scenáre dokopy | Orchestrace multi-agentného **predania** | 8094 |

> **Poznámka k agentovi na odporúčanie úloh.** `task-recommendation-agent.py` potrebuje
> `GITHUB_PERSONAL_ACCESS_TOKEN` vo vašom `.env` (vytvorte si ho na
> <https://github.com/settings/personal-access-tokens/new>). Číta nedávnu
> aktivitu vývojára na GitHub a odporúča 1–3 otvorené problémy, ktoré zodpovedajú — presne ako scénar 2.
> Toto je jediná ukážka, ktorá volá GitHub; ostatné potrebujú iba váš projekt Foundry.

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Vyhlásenie o zodpovednosti**:
Tento dokument bol preložený pomocou AI prekladateľskej služby [Co-op Translator](https://github.com/Azure/co-op-translator). Hoci sa snažíme o presnosť, vezmite prosím na vedomie, že automatické preklady môžu obsahovať chyby alebo nepresnosti. Pôvodný dokument v jeho natívnom jazyku by mal byť považovaný za autoritatívny zdroj. Pre kritické informácie sa odporúča profesionálny ľudský preklad. Nie sme zodpovední za žiadne nedorozumenia alebo nesprávne interpretácie vyplývajúce z použitia tohto prekladu.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->