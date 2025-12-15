<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:10:18+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "id"
}
-->
# Pelajaran 4: Penyebaran Agen dengan Azure AI Foundry Hosted Agents + ChatKit

Pelajaran ini menunjukkan cara menyebarkan alur kerja multi-agen ke Azure AI Foundry sebagai agen yang dihosting dan membuat frontend berbasis ChatKit untuk berinteraksi dengannya.

## Arsitektur

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

1. **Proyek Azure AI Foundry** di wilayah North Central US
2. **Azure CLI** yang sudah diautentikasi (`az login`)
3. **Azure Developer CLI** (`azd`) terpasang
4. **Python 3.12+** dan **Node.js 18+**
5. **Vector Store** yang dibuat dengan data karyawan

## Mulai Cepat

### 1. Atur Variabel Lingkungan

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edit .env dengan detail proyek Azure AI Foundry Anda
```

### 2. Sebarkan Hosted Agent

**Opsi A: Menggunakan Azure Developer CLI (Direkomendasikan)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opsi B: Menggunakan Docker + Azure Container Registry**

```bash
cd hosted-agent

# Bangun kontainer
docker build -t developer-onboarding-agent:latest .

# Tag untuk ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Dorong ke ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Deploy melalui portal Azure AI Foundry atau SDK
```

### 3. Mulai Backend ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Di Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server akan mulai di `http://localhost:8001`

### 4. Mulai Frontend ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Frontend akan mulai di `http://localhost:3000`

### 5. Uji Aplikasi

Buka `http://localhost:3000` di browser Anda dan coba pertanyaan berikut:

**Pencarian Karyawan:**
- "Saya baru di sini! Apakah ada yang pernah bekerja di Microsoft?"
- "Siapa yang memiliki pengalaman dengan Azure Functions?"

**Sumber Belajar:**
- "Buat jalur pembelajaran untuk Kubernetes"
- "Sertifikasi apa yang harus saya kejar untuk arsitektur cloud?"

**Bantuan Pengkodean:**
- "Bantu saya menulis kode Python untuk menghubungkan ke CosmosDB"
- "Tunjukkan cara membuat Azure Function"

**Pertanyaan Multi-Agen:**
- "Saya mulai sebagai insinyur cloud. Dengan siapa saya harus terhubung dan apa yang harus saya pelajari?"

## Struktur Proyek

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

## Alur Kerja Multi-Agen

Hosted agent menggunakan **HandoffBuilder** untuk mengatur empat agen khusus:

| Agen | Peran | Alat |
|-------|------|-------|
| **Triage Agent** | Koordinator - mengarahkan pertanyaan ke spesialis | Tidak ada |
| **Employee Search Agent** | Mencari rekan kerja dan anggota tim | HostedFileSearchTool (Vector Store) |
| **Learning Agent** | Membuat jalur pembelajaran dan rekomendasi | HostedMCPTool (Microsoft Learn) |
| **Coding Agent** | Menghasilkan contoh kode dan panduan | Tidak ada |

Alur kerja memungkinkan:
- Triage → Spesialis mana pun
- Spesialis → Spesialis lain (untuk pertanyaan terkait)
- Spesialis → Triage (untuk topik baru)

## Pemecahan Masalah

### Agen tidak merespons
- Pastikan hosted agent sudah disebarkan dan berjalan di Azure AI Foundry
- Periksa apakah `HOSTED_AGENT_NAME` dan `HOSTED_AGENT_VERSION` sesuai dengan penyebaran Anda

### Kesalahan vector store
- Pastikan `VECTOR_STORE_ID` sudah diatur dengan benar
- Verifikasi vector store berisi data karyawan

### Kesalahan autentikasi
- Jalankan `az login` untuk menyegarkan kredensial
- Pastikan Anda memiliki akses ke proyek Azure AI Foundry

## Sumber Daya

- [Dokumentasi Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Contoh Integrasi ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Penafian**:  
Dokumen ini telah diterjemahkan menggunakan layanan terjemahan AI [Co-op Translator](https://github.com/Azure/co-op-translator). Meskipun kami berupaya untuk mencapai akurasi, harap diingat bahwa terjemahan otomatis mungkin mengandung kesalahan atau ketidakakuratan. Dokumen asli dalam bahasa aslinya harus dianggap sebagai sumber yang sahih. Untuk informasi penting, disarankan menggunakan terjemahan profesional oleh manusia. Kami tidak bertanggung jawab atas kesalahpahaman atau salah tafsir yang timbul dari penggunaan terjemahan ini.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->