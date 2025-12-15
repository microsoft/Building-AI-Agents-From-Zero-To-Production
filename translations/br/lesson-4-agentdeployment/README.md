<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "3454eeec0053596d08ce81335a963ac6",
  "translation_date": "2025-12-12T19:01:57+00:00",
  "source_file": "lesson-4-agentdeployment/README.md",
  "language_code": "br"
}
-->
# Lesson 4: Implantação de Agente com Azure AI Foundry Hosted Agents + ChatKit

Esta lição demonstra como implantar um fluxo de trabalho multiagente no Azure AI Foundry como um agente hospedado e criar uma interface baseada em ChatKit para interagir com ele.

## Arquitetura

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

## Pré-requisitos

1. **Projeto Azure AI Foundry** na região North Central US
2. **Azure CLI** autenticado (`az login`)
3. **Azure Developer CLI** (`azd`) instalado
4. **Python 3.12+** e **Node.js 18+**
5. **Armazenamento Vetorial** criado com dados de funcionários

## Início Rápido

### 1. Configurar Variáveis de Ambiente

```bash
cd lesson-4-agentdeployment
cp .env.example .env
# Edite o .env com os detalhes do seu projeto Azure AI Foundry
```

### 2. Implantar o Agente Hospedado

**Opção A: Usando Azure Developer CLI (Recomendado)**

```bash
cd hosted-agent
azd auth login
azd agent deploy
```

**Opção B: Usando Docker + Azure Container Registry**

```bash
cd hosted-agent

# Construir o contêiner
docker build -t developer-onboarding-agent:latest .

# Tag para ACR
docker tag developer-onboarding-agent:latest <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Enviar para ACR
az acr login --name <your-acr>
docker push <your-acr>.azurecr.io/developer-onboarding-agent:latest

# Implantar via portal Azure AI Foundry ou SDK
```

### 3. Iniciar o Backend do ChatKit

```bash
cd chatkit-server
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

O servidor será iniciado em `http://localhost:8001`

### 4. Iniciar o Frontend do ChatKit

```bash
cd chatkit-server/frontend
npm install
npm run dev
```

O frontend será iniciado em `http://localhost:3000`

### 5. Testar a Aplicação

Abra `http://localhost:3000` no seu navegador e experimente estas consultas:

**Busca de Funcionários:**
- "Sou novo aqui! Alguém já trabalhou na Microsoft?"
- "Quem tem experiência com Azure Functions?"

**Recursos de Aprendizado:**
- "Crie um caminho de aprendizado para Kubernetes"
- "Quais certificações devo buscar para arquitetura de nuvem?"

**Ajuda com Código:**
- "Me ajude a escrever código Python para conectar ao CosmosDB"
- "Mostre como criar uma Azure Function"

**Consultas Multiagente:**
- "Estou começando como engenheiro de nuvem. Com quem devo me conectar e o que devo aprender?"

## Estrutura do Projeto

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

## O Fluxo de Trabalho Multiagente

O agente hospedado usa **HandoffBuilder** para orquestrar quatro agentes especializados:

| Agente | Função | Ferramentas |
|--------|--------|-------------|
| **Agente de Triagem** | Coordenador - direciona consultas para especialistas | Nenhuma |
| **Agente de Busca de Funcionários** | Encontra colegas e membros da equipe | HostedFileSearchTool (Armazenamento Vetorial) |
| **Agente de Aprendizado** | Cria caminhos de aprendizado e recomendações | HostedMCPTool (Microsoft Learn) |
| **Agente de Codificação** | Gera exemplos de código e orientações | Nenhuma |

O fluxo de trabalho permite:
- Triagem → Qualquer especialista
- Especialistas → Outros especialistas (para consultas relacionadas)
- Especialistas → Triagem (para novos tópicos)

## Solução de Problemas

### Agente não responde
- Verifique se o agente hospedado está implantado e em execução no Azure AI Foundry
- Confira se `HOSTED_AGENT_NAME` e `HOSTED_AGENT_VERSION` correspondem à sua implantação

### Erros no armazenamento vetorial
- Certifique-se de que `VECTOR_STORE_ID` está configurado corretamente
- Verifique se o armazenamento vetorial contém os dados dos funcionários

### Erros de autenticação
- Execute `az login` para atualizar as credenciais
- Garanta que você tenha acesso ao projeto Azure AI Foundry

## Recursos

- [Documentação do Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Exemplo de Integração ChatKit](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

<!-- CO-OP TRANSLATOR DISCLAIMER START -->
**Aviso Legal**:  
Este documento foi traduzido utilizando o serviço de tradução por IA [Co-op Translator](https://github.com/Azure/co-op-translator). Embora nos esforcemos para garantir a precisão, esteja ciente de que traduções automáticas podem conter erros ou imprecisões. O documento original em seu idioma nativo deve ser considerado a fonte autorizada. Para informações críticas, recomenda-se a tradução profissional realizada por humanos. Não nos responsabilizamos por quaisquer mal-entendidos ou interpretações incorretas decorrentes do uso desta tradução.
<!-- CO-OP TRANSLATOR DISCLAIMER END -->