<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:10:51+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "ms"
}
-->
# Lesson 4: Penyebaran Ejen dengan Azure AI Foundry Hosted Agents + ChatKit

Pelajaran ini menunjukkan cara menyebarkan aliran kerja berbilang ejen ke Azure AI Foundry sebagai ejen yang dihoskan dan mencipta frontend berasaskan ChatKit untuk berinteraksi dengannya.

## Seni Bina

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

## Prasyarat

1. **Projek Azure AI Foundry** di rantau North Central US
2. **Azure CLI** yang telah diautentikasi (`az login`)
3. **Azure Developer CLI** (`azd`) dipasang
4. **Python 3.12+** dan **Node.js 18+**
5. **Vector Store** yang dibuat dengan data pekerja

## Mula Pantas

### 1. Tetapkan Pembolehubah Persekitaran

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edit .env dengan butiran projek Azure AI Foundry anda
```

### 2. Sebarkan Ejen yang Dihoskan

**Pilihan A: Menggunakan Azure Developer CLI (Disyorkan)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Pilihan B: Menggunakan Docker + Azure Container Registry**

```bash
cd hosted-agent

# Bina bekas
docker build -t developer-onboarding-agent:latest .

# Tag untuk ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Tolak ke ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Lancarkan melalui portal Azure AI Foundry atau SDK
```

### 3. Mulakan Backend ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Pada Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Pelayan akan bermula di `http://localhost:8001`

### 4. Mulakan Frontend ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend akan bermula di `http://localhost:3000`

### 5. Uji Aplikasi

Buka `http://localhost:3000` dalam pelayar anda dan cuba pertanyaan ini:

**Carian Pekerja:**
- "Saya baru di sini! Adakah sesiapa pernah bekerja di Microsoft?"
- "Siapa yang mempunyai pengalaman dengan Azure Functions?"

**Sumber Pembelajaran:**
- "Cipta laluan pembelajaran untuk Kubernetes"
- "Apakah sijil yang patut saya kejar untuk seni bina awan?"

**Bantuan Pengkodan:**
- "Bantu saya menulis kod Python untuk menyambung ke CosmosDB"
- "Tunjukkan cara mencipta Azure Function"

**Pertanyaan Berbilang Ejen:**
- "Saya mula sebagai jurutera awan. Dengan siapa saya patut berhubung dan apa yang patut saya pelajari?"

## Struktur Projek

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

## Aliran Kerja Berbilang Ejen

Ejen yang dihoskan menggunakan **HandoffBuilder** untuk mengatur empat ejen khusus:

| Ejen | Peranan | Alat |
|-------|------|-------|
| **Ejen Triage** | Penyelarasan - mengarahkan pertanyaan kepada pakar | Tiada |
| **Ejen Carian Pekerja** | Mencari rakan sekerja dan ahli pasukan | HostedFileSearchTool (Vector Store) |
| **Ejen Pembelajaran** | Mencipta laluan pembelajaran dan cadangan | HostedMCPTool (Microsoft Learn) |
| **Ejen Pengkodan** | Menjana contoh kod dan panduan | Tiada |

Aliran kerja membenarkan:
- Triage → Mana-mana pakar
- Pakar → Pakar lain (untuk pertanyaan berkaitan)
- Pakar → Triage (untuk topik baru)

## Penyelesaian Masalah

### Ejen tidak memberi respons
- Sahkan ejen yang dihoskan telah disebarkan dan berjalan di Azure AI Foundry
- Semak `HOSTED_AGENT_NAME` dan `HOSTED_AGENT_VERSION` sepadan dengan penyebaran anda

### Ralat vector store
- Pastikan `VECTOR_STORE_ID` ditetapkan dengan betul
- Sahkan vector store mengandungi data pekerja

### Ralat pengesahan
- Jalankan `az login` untuk menyegarkan kelayakan
- Pastikan anda mempunyai akses ke projek Azure AI Foundry

## Sumber

- [Dokumentasi Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Contoh Integrasi ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan perkhidmatan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Walaupun kami berusaha untuk ketepatan, sila ambil perhatian bahawa terjemahan automatik mungkin mengandungi kesilapan atau ketidaktepatan. Dokumen asal dalam bahasa asalnya harus dianggap sebagai sumber yang sahih. Untuk maklumat penting, terjemahan profesional oleh manusia adalah disyorkan. Kami tidak bertanggungjawab atas sebarang salah faham atau salah tafsir yang timbul daripada penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->