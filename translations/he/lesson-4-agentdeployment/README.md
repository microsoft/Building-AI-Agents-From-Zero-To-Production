<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:09:07+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "he"
}
-->
# שיעור 4: פריסת סוכן עם Azure AI Foundry Hosted Agents + ChatKit

שיעור זה מדגים כיצד לפרוס תהליך עבודה רב-סוכני ל-Azure AI Foundry כסוכן מתארח וליצור ממשק קדמי מבוסס ChatKit כדי לתקשר איתו.

## ארכיטקטורה

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

## דרישות מוקדמות

1. **פרויקט Azure AI Foundry** באזור North Central US
2. **Azure CLI** מאומת (`az login`)
3. **Azure Developer CLI** (`azd`) מותקן
4. **Python 3.12+** ו-**Node.js 18+**
5. **מאגר וקטורים** שנוצר עם נתוני עובדים

## התחלה מהירה

### 1. הגדרת משתני סביבה

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# ערוך את קובץ .env עם פרטי פרויקט Azure AI Foundry שלך
```

### 2. פריסת הסוכן המתארח

**אפשרות א: שימוש ב-Azure Developer CLI (מומלץ)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**אפשרות ב: שימוש ב-Docker + Azure Container Registry**

```bash
cd hosted-agent

# לבנות את המכולה
docker build -t developer-onboarding-agent:latest .

# תג עבור ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# לדחוף ל-ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# לפרוס דרך פורטל Azure AI Foundry או SDK
```

### 3. הפעלת ה-Backend של ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # ב-Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

השרת יופעל בכתובת `http://localhost:8001`

### 4. הפעלת ה-Frontend של ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

הממשק הקדמי יופעל בכתובת `http://localhost:3000`

### 5. בדיקת היישום

פתח את `http://localhost:3000` בדפדפן ונסה את השאילתות הבאות:

**חיפוש עובדים:**
- "אני חדש כאן! האם מישהו עבד ב-Microsoft?"
- "מי יש לו ניסיון עם Azure Functions?"

**משאבי למידה:**
- "צור מסלול למידה עבור Kubernetes"
- "אילו הסמכות כדאי לי לרכוש לארכיטקטורת ענן?"

**עזרה בקידוד:**
- "עזור לי לכתוב קוד Python להתחברות ל-CosmosDB"
- "הראה לי איך ליצור Azure Function"

**שאילתות רב-סוכניות:**
- "אני מתחיל כמהנדס ענן. עם מי כדאי לי להתחבר ומה כדאי לי ללמוד?"

## מבנה הפרויקט

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

## תהליך העבודה הרב-סוכני

הסוכן המתארח משתמש ב-**HandoffBuilder** כדי לתזמן ארבעה סוכנים מתמחים:

| סוכן | תפקיד | כלים |
|-------|------|-------|
| **סוכן מיון** | מתאם - מנתב שאילתות למומחים | אין |
| **סוכן חיפוש עובדים** | מוצא עמיתים וחברי צוות | HostedFileSearchTool (מאגר וקטורים) |
| **סוכן למידה** | יוצר מסלולי למידה והמלצות | HostedMCPTool (Microsoft Learn) |
| **סוכן קידוד** | מייצר דוגמאות קוד והנחיות | אין |

תהליך העבודה מאפשר:
- מיון → כל מומחה
- מומחים → מומחים אחרים (לשאילתות קשורות)
- מומחים → מיון (לנושאים חדשים)

## פתרון בעיות

### הסוכן לא מגיב
- ודא שהסוכן המתארח פרוס ופועל ב-Azure AI Foundry
- בדוק ש-`HOSTED_AGENT_NAME` ו-`HOSTED_AGENT_VERSION` תואמים לפריסה שלך

### שגיאות במאגר הווקטורים
- ודא ש-`VECTOR_STORE_ID` מוגדר נכון
- וודא שמאגר הווקטורים מכיל את נתוני העובדים

### שגיאות אימות
- הרץ `az login` לרענון האישורים
- ודא שיש לך גישה לפרויקט Azure AI Foundry

## משאבים

- [תיעוד Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [דוגמת אינטגרציה של ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי אדם. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->