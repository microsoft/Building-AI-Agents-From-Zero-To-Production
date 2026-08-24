# Les 1: Ontwerp van AI-Agent

Welkom bij de eerste les van de "Bouwen van een AI-Agent van Nul tot Productie Cursus"!

In deze les behandelen we:

- Definiëren wat AI-Agents zijn
  
- Bespreken van de AI-Agent Applicatie die we aan het bouwen zijn  

- Identificeren van de vereiste tools en diensten voor elke agent
  
- Architectuur van onze Agent Applicatie
  
Laten we beginnen met het definiëren wat een agent is en waarom we ze binnen een applicatie zouden gebruiken.

> **Voordat je aan de cursus begint.** Deze eerste les is conceptueel — er is geen code om uit te voeren.
> Vanaf [Les 2](../lesson-2-agent-development/README.md) heb je nodig: een **Azure
> abonnement** met toegang tot **Microsoft Foundry**, een gedeployed **GPT-5 series model** (bijv.
> `gpt-5.1` — vermijd het gepensioneerde GPT-4o / GPT-4.1), **Python 3.12+** en de **Azure CLI**
> (`az login`). Zie [Wat Je Nodig Hebt](../README.md#what-you-need) in de cursus-README voor de volledige
> lijst en links.

## Wat zijn AI-Agents?

![Wat zijn AI-Agents?](../../../translated_images/nl/what-are-ai-agents.47a544a1d03481ab.webp)

Als dit je eerste keer is dat je onderzoekt hoe je een AI-Agent bouwt, heb je wellicht vragen over hoe je precies definieert wat een AI-Agent is.

Voor een eenvoudige manier om te definiëren wat een AI-Agent is aan de hand van de componenten die het maakt:

**Groot Taalmodel** - Het LLM zal zowel het vermogen aansturen om natuurlijke taal van de gebruiker te verwerken om de taak die zij willen voltooien te interpreteren, als om de beschrijvingen van de beschikbare tools te interpreteren om die taken uit te voeren.

**Tools** - Dit zullen functies, API's, gegevensopslagplaatsen en andere diensten zijn die het LLM kan kiezen om te gebruiken om de door de gebruiker gevraagde taken te voltooien.

**Geheugen** - Dit is hoe we zowel korte- als lange-termijn interacties tussen de AI-Agent en de gebruiker opslaan. Het opslaan en opvragen van deze informatie is belangrijk om verbeteringen aan te brengen en gebruikersvoorkeuren in de loop der tijd te bewaren.

## Onze AI-Agent Use Case

![Wat Bouwen We?](../../../translated_images/nl/what-are-we-building.1ff3b9a752eb8570.webp)

Voor deze cursus gaan we een AI-Agent applicatie bouwen die nieuwe ontwikkelaars helpt om zich aan te sluiten bij ons AI-Agent Ontwikkelingsteam!

Voordat we enige ontwikkelwerk doen, is de eerste stap voor het maken van een succesvolle AI-Agent applicatie het definiëren van heldere scenario's over hoe we verwachten dat onze gebruikers werken met onze AI-Agents.

Voor deze applicatie werken we met deze scenario's:

**Scenario 1**: Een nieuwe medewerker komt bij onze organisatie en wil meer weten over het team waar zij zich bij hebben aangesloten en hoe ze contact kunnen maken.

**Scenario 2:** Een nieuwe medewerker wil weten wat de beste eerste taak zou zijn om aan te beginnen.

**Scenario 3:** Een nieuwe medewerker wil leermaterialen en codevoorbeelden verzamelen om hen te helpen bij het starten en voltooien van deze taak.

## Identificeren van de Tools en Diensten

Nu we deze scenario's hebben opgesteld, is de volgende stap om ze te koppelen aan de tools en diensten die onze AI-agents nodig zullen hebben om deze taken uit te voeren.

Dit proces valt onder de categorie Context Engineering, omdat we ons gaan richten op het zorgen dat onze AI-Agents de juiste context op het juiste moment hebben om de taken te voltooien.

Laten we dit scenario voor scenario doen en goed agentontwerp uitvoeren door de taken, tools en gewenste uitkomsten van elke agent te benoemen.

![Agent Ontwerp](../../../translated_images/nl/agent-design.07edb7ae37f47803.webp)

### Scenario 1 - Medewerker Zoekagent

**Taak** - Beantwoorden van vragen over medewerkers binnen de organisatie zoals toetredingsdatum, huidig team, locatie en laatste functie.

**Tools** - Gegevensopslag van huidige medewerkerslijst en organisatiekaart

**Uitkomsten** - In staat zijn informatie uit de gegevensopslag op te halen om algemene organisatorische vragen en specifieke vragen over medewerkers te beantwoorden.

### Scenario 2 - Taakaanbeveling Agent

**Taak** - Op basis van de ontwikkelaarservaring van de nieuwe medewerker 1-3 issues voorstellen waar de nieuwe medewerker aan kan werken.

**Tools** - GitHub MCP Server om open issues op te halen en een ontwikkelaarsprofiel op te bouwen

**Uitkomsten** - In staat zijn de laatste 5 commits van een GitHub-profiel en open issues van een GitHub-project te lezen en aanbevelingen te doen op basis van een match

### Scenario 3 - Code Assistent Agent

**Taak** - Op basis van de Open Issues die zijn aanbevolen door de "Taakaanbeveling" Agent, bronnen onderzoeken en codefragmenten genereren om de medewerker te helpen.

**Tools** - Microsoft Learn MCP om bronnen te vinden en Code Interpreter om aangepaste codefragmenten te genereren.

**Uitkomsten** - Als de gebruiker om extra hulp vraagt, moet de workflow de Learn MCP Server gebruiken om links en fragmenten naar bronnen te verstrekken en vervolgens overdragen aan de Code Interpreter agent om kleine codefragmenten met uitleg te genereren.

## Architectuur van onze Agent Applicatie

Nu we elk van onze Agents hebben gedefinieerd, laten we een architectuurdiagram maken dat ons helpt te begrijpen hoe elke agent samen en apart zal werken, afhankelijk van de taak:

![Agent Architectuur](../../../translated_images/nl/agent-architecture.4fd5efa371e77a3c.webp)

## Volgende Stappen

Nu we elk agent en ons agentensysteem hebben ontworpen, gaan we door naar de volgende les waar we elk van deze agents gaan ontwikkelen!

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Disclaimer**:
Dit document is vertaald met behulp van de AI vertaaldienst [Co-op Translator](https://github.com/Azure/co-op-translator). Hoewel we streven naar nauwkeurigheid, dient u er rekening mee te houden dat geautomatiseerde vertalingen fouten of onnauwkeurigheden kunnen bevatten. Het originele document in de oorspronkelijke taal moet worden beschouwd als de gezaghebbende bron. Voor kritieke informatie wordt professionele menselijke vertaling aanbevolen. Wij zijn niet aansprakelijk voor eventuele misverstanden of verkeerde interpretaties die voortvloeien uit het gebruik van deze vertaling.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->