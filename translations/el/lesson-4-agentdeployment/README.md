<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:04:45+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "el"
}
-->
# Μάθημα 4: Ανάπτυξη Πράκτορα με Azure AI Foundry Hosted Agents + ChatKit

Αυτό το μάθημα δείχνει πώς να αναπτύξετε μια ροή εργασίας πολλαπλών πρακτόρων στο Azure AI Foundry ως φιλοξενούμενο πράκτορα και να δημιουργήσετε ένα frontend βασισμένο στο ChatKit για αλληλεπίδραση με αυτόν.

## Αρχιτεκτονική

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User's Browser                               │
│                    (ChatKit React Frontend)                          │
│                      localhost:3000                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTP/SSE
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ChatKit Backend Server                           │
│                    (FastAPI + SQLite Store)                          │
│                      localhost:8001                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ Azure AI Responses API
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry                                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │               Hosted Multi-Agent Workflow                      │  │
│  │  ┌─────────────┐  ┌──────────────────┐  ┌───────────────┐     │  │
│  │  │   Triage    │──│ Employee Search  │  │   Learning    │     │  │
│  │  │   Agent     │  │     Agent        │  │    Agent      │     │  │
│  │  │(Coordinator)│  │ (Vector Store)   │  │ (MCP Tool)    │     │  │
│  │  └──────┬──────┘  └──────────────────┘  └───────────────┘     │  │
│  │         │         ┌──────────────────┐                         │  │
│  │         └─────────│  Coding Agent    │                         │  │
│  │                   │ (Code Generation)│                         │  │
│  │                   └──────────────────┘                         │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Προαπαιτούμενα

1. **Έργο Azure AI Foundry** στην περιοχή North Central US
2. **Azure CLI** με πιστοποίηση (`az login`)
3. **Azure Developer CLI** (`azd`) εγκατεστημένο
4. **Python 3.12+** και **Node.js 18+**
5. **Vector Store** δημιουργημένο με δεδομένα υπαλλήλων

## Γρήγορη Εκκίνηση

### 1. Ορισμός Μεταβλητών Περιβάλλοντος

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Επεξεργαστείτε το .env με τις λεπτομέρειες του έργου σας Azure AI Foundry
```

### 2. Ανάπτυξη του Φιλοξενούμενου Πράκτορα

**Επιλογή Α: Χρήση Azure Developer CLI (Συνιστάται)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Επιλογή Β: Χρήση Docker + Azure Container Registry**

```bash
cd hosted-agent

# Δημιουργήστε το κοντέινερ
docker build -t developer-onboarding-agent:latest .

# Ετικέτα για ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Σπρώξτε στο ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Αναπτύξτε μέσω της πύλης Azure AI Foundry ή SDK
```

### 3. Εκκίνηση του Backend του ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Σε Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Ο διακομιστής θα ξεκινήσει στο `http://localhost:8001`

### 4. Εκκίνηση του Frontend του ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Το frontend θα ξεκινήσει στο `http://localhost:3000`

### 5. Δοκιμή της Εφαρμογής

Ανοίξτε το `http://localhost:3000` στον περιηγητή σας και δοκιμάστε αυτά τα ερωτήματα:

**Αναζήτηση Υπαλλήλων:**
- "Είμαι καινούριος εδώ! Έχει δουλέψει κανείς στη Microsoft;"
- "Ποιος έχει εμπειρία με τις Azure Functions;"

**Πόροι Μάθησης:**
- "Δημιούργησε μια διαδρομή μάθησης για Kubernetes"
- "Ποιες πιστοποιήσεις πρέπει να ακολουθήσω για αρχιτεκτονική cloud;"

**Βοήθεια στον Κώδικα:**
- "Βοήθησέ με να γράψω κώδικα Python για σύνδεση με CosmosDB"
- "Δείξε μου πώς να δημιουργήσω μια Azure Function"

**Ερωτήματα Πολλαπλών Πρακτόρων:**
- "Ξεκινάω ως μηχανικός cloud. Με ποιον πρέπει να συνδεθώ και τι πρέπει να μάθω;"

## Δομή Έργου

```
lesson-4-agentdeployment/
├── .env.example                 # Environment variables template
├── implementation-plan.md       # Detailed implementation guide
├── README.md                    # This file
├── hosted-agent/               # Azure AI Foundry hosted agent
│   ├── main.py                 # Multi-agent workflow implementation
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Container definition
│   └── agent.yaml              # Agent deployment configuration
└── chatkit-server/             # ChatKit server application
    ├── app.py                  # FastAPI backend
    ├── store.py                # SQLite persistence layer
    ├── requirements.txt        # Python dependencies
    └── frontend/               # React frontend
        ├── package.json
        ├── vite.config.ts
        ├── tsconfig.json
        ├── index.html
        └── src/
            ├── main.tsx
            ├── App.tsx
            ├── App.css
            └── index.css
```

## Η Ροή Εργασίας Πολλαπλών Πρακτόρων

Ο φιλοξενούμενος πράκτορας χρησιμοποιεί το **HandoffBuilder** για να οργανώσει τέσσερις εξειδικευμένους πράκτορες:

| Πράκτορας | Ρόλος | Εργαλεία |
|-----------|-------|----------|
| **Triage Agent** | Συντονιστής - δρομολογεί ερωτήματα σε ειδικούς | Κανένα |
| **Employee Search Agent** | Βρίσκει συναδέλφους και μέλη ομάδας | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Δημιουργεί διαδρομές μάθησης και προτάσεις | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Δημιουργεί παραδείγματα κώδικα και καθοδήγηση | Κανένα |

Η ροή εργασίας επιτρέπει:
- Triage → Οποιονδήποτε ειδικό
- Ειδικούς → Άλλους ειδικούς (για σχετικές ερωτήσεις)
- Ειδικούς → Triage (για νέα θέματα)

## Αντιμετώπιση Προβλημάτων

### Ο πράκτορας δεν ανταποκρίνεται
- Επαληθεύστε ότι ο φιλοξενούμενος πράκτορας έχει αναπτυχθεί και λειτουργεί στο Azure AI Foundry
- Ελέγξτε ότι το `HOSTED_AGENT_NAME` και το `HOSTED_AGENT_VERSION` ταιριάζουν με την ανάπτυξή σας

### Σφάλματα Vector store
- Βεβαιωθείτε ότι το `VECTOR_STORE_ID` έχει οριστεί σωστά
- Επαληθεύστε ότι το vector store περιέχει τα δεδομένα υπαλλήλων

### Σφάλματα πιστοποίησης
- Εκτελέστε `az login` για ανανέωση των διαπιστευτηρίων
- Βεβαιωθείτε ότι έχετε πρόσβαση στο έργο Azure AI Foundry

## Πόροι

- [Τεκμηρίωση Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Παράδειγμα Ενσωμάτωσης ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Αποποίηση ευθυνών**:  
Αυτό το έγγραφο έχει μεταφραστεί χρησιμοποιώντας την υπηρεσία αυτόματης μετάφρασης AI [Co-op Translator](https://github.com/Azure/co-op-translator). Παρόλο που επιδιώκουμε την ακρίβεια, παρακαλούμε να λάβετε υπόψη ότι οι αυτόματες μεταφράσεις ενδέχεται να περιέχουν λάθη ή ανακρίβειες. Το πρωτότυπο έγγραφο στη μητρική του γλώσσα πρέπει να θεωρείται η αυθεντική πηγή. Για κρίσιμες πληροφορίες, συνιστάται επαγγελματική ανθρώπινη μετάφραση. Δεν φέρουμε ευθύνη για τυχόν παρεξηγήσεις ή λανθασμένες ερμηνείες που προκύπτουν από τη χρήση αυτής της μετάφρασης.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->