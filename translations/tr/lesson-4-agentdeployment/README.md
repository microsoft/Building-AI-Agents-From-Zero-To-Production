<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:03:53+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "tr"
}
-->
# Ders 4: Azure AI Foundry Barındırılan Ajanlar + ChatKit ile Ajan Dağıtımı

Bu ders, çok ajanlı bir iş akışını Azure AI Foundry'ye barındırılan ajan olarak nasıl dağıtacağınızı ve onunla etkileşim kurmak için ChatKit tabanlı bir ön yüz oluşturmayı gösterir.

## Mimari

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

## Ön Koşullar

1. Kuzey Orta ABD bölgesinde **Azure AI Foundry Projesi**
2. Kimlik doğrulaması yapılmış **Azure CLI** (`az login`)
3. Yüklü **Azure Developer CLI** (`azd`)
4. **Python 3.12+** ve **Node.js 18+**
5. Çalışan verileri ile oluşturulmuş **Vektör Deposu**

## Hızlı Başlangıç

### 1. Ortam Değişkenlerini Ayarlayın

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# .env dosyasını Azure AI Foundry proje detaylarınızla düzenleyin
```

### 2. Barındırılan Ajanı Dağıtın

**Seçenek A: Azure Developer CLI Kullanarak (Önerilen)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Seçenek B: Docker + Azure Container Registry Kullanarak**

```bash
cd hosted-agent

# Konteyneri oluştur
docker build -t developer-onboarding-agent:latest .

# ACR için etiketle
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# ACR'ye gönder
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Azure AI Foundry portalı veya SDK üzerinden dağıtım yap
```

### 3. ChatKit Arka Ucunu Başlatın

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # Windows'ta: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Sunucu `http://localhost:8001` adresinde başlayacaktır.

### 4. ChatKit Ön Ucunu Başlatın

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

Ön yüz `http://localhost:3000` adresinde başlayacaktır.

### 5. Uygulamayı Test Edin

Tarayıcınızda `http://localhost:3000` adresini açın ve şu sorguları deneyin:

**Çalışan Arama:**
- "Burada yeniyim! Microsoft'ta çalışan var mı?"
- "Azure Functions konusunda deneyimi olan kim?"

**Öğrenme Kaynakları:**
- "Kubernetes için bir öğrenme yolu oluştur"
- "Bulut mimarisi için hangi sertifikaları almalıyım?"

**Kodlama Yardımı:**
- "CosmosDB'ye bağlanmak için Python kodu yazmama yardım et"
- "Bir Azure Function nasıl oluşturulur göster"

**Çok Ajanlı Sorgular:**
- "Bulut mühendisi olarak başlıyorum. Kiminle bağlantı kurmalıyım ve ne öğrenmeliyim?"

## Proje Yapısı

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

## Çok Ajanlı İş Akışı

Barındırılan ajan, dört uzmanlaşmış ajanı düzenlemek için **HandoffBuilder** kullanır:

| Ajan | Rol | Araçlar |
|-------|------|-------|
| **Triage Ajanı** | Koordinatör - sorguları uzmanlara yönlendirir | Yok |
| **Çalışan Arama Ajanı** | Meslektaşları ve ekip üyelerini bulur | HostedFileSearchTool (Vektör Deposu) |
| **Öğrenme Ajanı** | Öğrenme yolları ve öneriler oluşturur | HostedMCPTool (Microsoft Learn) |
| **Kodlama Ajanı** | Kod örnekleri ve rehberlik üretir | Yok |

İş akışı şunlara izin verir:
- Triage → Herhangi bir uzman
- Uzmanlar → Diğer uzmanlar (ilgili sorgular için)
- Uzmanlar → Triage (yeni konular için)

## Sorun Giderme

### Ajan yanıt vermiyor
- Barındırılan ajanın Azure AI Foundry'de dağıtılıp çalıştığını doğrulayın
- `HOSTED_AGENT_NAME` ve `HOSTED_AGENT_VERSION` değerlerinin dağıtımınızla eşleştiğini kontrol edin

### Vektör deposu hataları
- `VECTOR_STORE_ID` değerinin doğru ayarlandığından emin olun
- Vektör deposunun çalışan verilerini içerdiğini doğrulayın

### Kimlik doğrulama hataları
- Kimlik bilgilerini yenilemek için `az login` komutunu çalıştırın
- Azure AI Foundry projesine erişiminizin olduğundan emin olun

## Kaynaklar

- [Azure AI Foundry Barındırılan Ajanlar Belgeleri](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Ajan Çerçevesi](https://github.com/microsoft/agent-framework)
- [ChatKit Entegrasyon Örneği](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Feragatname**:  
Bu belge, AI çeviri servisi [Co-op Translator](https://github.com/Azure/co-op-translator) kullanılarak çevrilmiştir. Doğruluk için çaba gösterilse de, otomatik çevirilerin hatalar veya yanlışlıklar içerebileceğini lütfen unutmayın. Orijinal belge, kendi dilinde yetkili kaynak olarak kabul edilmelidir. Kritik bilgiler için profesyonel insan çevirisi önerilir. Bu çevirinin kullanımı sonucu oluşabilecek yanlış anlamalar veya yorum hatalarından sorumlu değiliz.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->