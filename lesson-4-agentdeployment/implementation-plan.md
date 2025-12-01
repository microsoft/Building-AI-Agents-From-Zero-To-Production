# Implementation Plan: Azure AI Foundry Hosted Agents with ChatKit

## Overview

This implementation plan outlines the steps to deploy a hosted agent on Azure AI Foundry and create a local ChatKit frontend that communicates with the hosted agent. The solution combines:

1. **Azure AI Foundry Hosted Agents** - Deploy containerized AI agents to Microsoft's managed platform
2. **ChatKit Frontend** - A React-based UI for interacting with the hosted agent
3. **Microsoft Agent Framework** - The underlying agent orchestration framework

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LOCAL DEVELOPMENT                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────┐         ┌──────────────────────────┐                │
│   │   React Frontend │  HTTP   │   FastAPI Backend        │                │
│   │   (ChatKit UI)   │ ──────> │   (Local ChatKit Server) │                │
│   │   localhost:5171 │         │   localhost:8001         │                │
│   └──────────────────┘         └───────────┬──────────────┘                │
│                                            │                                │
└────────────────────────────────────────────┼────────────────────────────────┘
                                             │ HTTPS (Azure SDK)
                                             ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AZURE AI FOUNDRY                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────┐         │
│   │                    Hosted Agent Service                       │         │
│   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │         │
│   │   │ Container Image │  │ Agent Runtime   │  │ Model (GPT) │ │         │
│   │   │ (Azure ACR)     │  │ (Auto-scaled)   │  │             │ │         │
│   │   └─────────────────┘  └─────────────────┘  └─────────────┘ │         │
│   └──────────────────────────────────────────────────────────────┘         │
│                                                                             │
│   ┌─────────────────────┐    ┌─────────────────────┐                       │
│   │ Azure Container     │    │ Application         │                       │
│   │ Registry (ACR)      │    │ Insights (Tracing)  │                       │
│   └─────────────────────┘    └─────────────────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Azure Resources Required
- [ ] Microsoft Foundry Project (Azure AI Foundry)
- [ ] Azure Container Registry (ACR)
- [ ] Azure OpenAI Service with deployed models (e.g., `gpt-4o`)
- [ ] Azure CLI installed and authenticated (`az login`)

### Local Development Tools
- [ ] Python 3.10+
- [ ] Node.js 18.18+ and npm 9+
- [ ] Docker (for building container images)
- [ ] Azure Developer CLI (`azd`) - optional but recommended

### Azure Role Requirements
- **Azure AI User** role on Foundry resource
- **Container Registry Repository Reader** role on ACR
- **Owner** or **User Access Administrator** on ACR (for role assignment)

---

## Implementation Steps

### Phase 1: Project Setup and Environment Configuration

#### Step 1.1: Create Project Structure
**Status**: 🔲 Not Started

Create the following folder structure inside `lesson-4-agentdeployment/`:

```
lesson-4-agentdeployment/
├── agent-deployment.py          # Existing file (to be refactored)
├── implementation-plan.md       # This file
├── hosted-agent/
│   ├── main.py                  # Hosted agent code
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Container build file
│   └── agent.yaml               # Agent definition for azd
├── chatkit-server/
│   ├── app.py                   # FastAPI ChatKit server
│   ├── store.py                 # SQLite storage implementation
│   ├── requirements.txt         # Python dependencies
│   └── frontend/
│       ├── package.json         # Node.js dependencies
│       ├── vite.config.ts       # Vite configuration
│       ├── index.html           # HTML template
│       └── src/
│           ├── main.tsx         # React entry point
│           └── App.tsx          # ChatKit UI component
└── .env.example                 # Environment variables template
```

#### Step 1.2: Configure Environment Variables
**Status**: 🔲 Not Started

Create `.env` file with required variables:

```bash
# Azure AI Foundry
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o

# Azure Container Registry
AZURE_CONTAINER_REGISTRY=your-registry.azurecr.io

# Hosted Agent Configuration
HOSTED_AGENT_NAME=developer-onboarding-agent
```

---

### Phase 2: Create the Hosted Multi-Agent Workflow

The hosted agent will include the **complete multi-agent handoff workflow** from `agent-deployment.py`:

- **Triage Agent** - Coordinator that routes requests to specialists
- **Employee Search Agent** - Searches employee data using file search tool
- **Learning Agent** - Creates learning paths using Microsoft Learn MCP
- **Coding Agent** - Generates code samples

#### Step 2.1: Implement the Hosted Agent Code
**Status**: 🔲 Not Started

Create `hosted-agent/main.py` - The complete multi-agent workflow deployed to Azure AI Foundry:

```python
"""
Developer Onboarding Multi-Agent Workflow - Hosted Agent

This hosted agent implements the complete developer onboarding workflow with:
- Triage Agent: Routes requests to appropriate specialists
- Employee Search Agent: Finds colleague information using file search
- Learning Agent: Creates personalized learning paths using Microsoft Learn MCP
- Coding Agent: Generates code samples and examples

The workflow uses HandoffBuilder pattern for intelligent routing between agents.
"""

import os
from agent_framework import (
    ChatMessage,
    HandoffBuilder,
    HostedFileSearchTool,
    HostedMCPTool,
    HostedVectorStoreContent,
    Role,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity import DefaultAzureCredential


def create_triage_agent(client: AzureOpenAIChatClient):
    """Create the Triage Agent - The Coordinator."""
    return client.create_agent(
        name="triage-agent",
        instructions="""You are the Developer Onboarding Assistant - a friendly coordinator helping new developers get settled at their new company.

Your role is to understand what the new developer needs and route them to the right specialist:

1. **Organizational Questions** → Hand off to employee_search_agent
   - Questions about coworkers, teams, managers
   - Finding people from the same former company
   - Understanding the org structure
   - Examples: "Who is on my team?", "Is anyone else from my former company here?", "Who manages the AI team?"

2. **Training & Learning** → Hand off to learning_agent
   - Creating learning paths and training plans
   - Finding documentation and tutorials
   - Understanding technologies used at the company
   - Examples: "I need to learn Azure", "Create a training plan for Python", "What should I learn first?"

3. **Coding Help & Code Samples** → Hand off to learning_agent FIRST
   - When users need code samples or coding assistance
   - The learning agent will gather relevant documentation
   - Then it will hand off to coding_agent to generate the actual code
   - Examples: "Show me how to write an Azure Function", "I need code for connecting to CosmosDB"

When you receive a request:
1. Greet the user warmly if it's their first message
2. Understand their specific need
3. Provide a brief acknowledgment of what they're asking
4. Call the appropriate handoff tool to route to the specialist

Always be encouraging and helpful - remember, this person is new and might feel overwhelmed!

Handoff tools available:
- handoff_to_employee_search_agent - For organizational and people questions
- handoff_to_learning_agent - For training, documentation, AND coding help
- handoff_to_coding_agent - Only for direct code generation
""",
    )


def create_employee_search_agent(client: AzureOpenAIChatClient):
    """Create the Employee Search Agent - Organizational Knowledge Specialist."""
    # Create the file search tool with pre-created vector store
    file_search_tool = HostedFileSearchTool(
        inputs=[
            HostedVectorStoreContent(
                vector_store_id=os.environ.get("VECTOR_STORE_ID", "")
            )
        ]
    )

    return client.create_agent(
        name="employee-search-agent",
        instructions="""You are the Employee Search Specialist for the Developer Onboarding program at Zava, a software company.

You help new developers learn about their coworkers and the organization structure.

Use the file search tool to find information about employees when asked questions like:
- "Is there anyone from my former company here?" (Note: The current user is "New Employee" who came from LinkedIn)
- "Who was the most recent joiner before me?"
- "Who is the manager for the AI Engineering Team?"
- "List all employees from Microsoft"
- "Who works on the Platform team?"

When answering questions about "my former company", remember that you are helping "New Employee" 
who previously worked at LinkedIn. Search for employees who also came from LinkedIn.

When asked questions about employees:
- Use the file search tool to search through the employee directory
- Provide helpful details like team, role, former company, and join date
- Be warm and welcoming - help them feel connected to their new colleagues

After answering organizational questions, ask if they need help with anything else:
- Learning resources for technologies used at the company
- Code samples for common tasks
- More information about specific people or teams""",
        tools=[file_search_tool],
    )


def create_learning_agent(client: AzureOpenAIChatClient):
    """Create the Learning Agent - Training & Documentation Specialist."""
    mcp_tool = HostedMCPTool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
        approval_mode="never_require",
    )

    return client.create_agent(
        name="learning-agent",
        instructions="""You are the Learning Path Specialist for the Developer Onboarding program.

You help new developers create personalized training plans and find relevant documentation.

**For Training/Documentation Requests:**
1. Understand their learning goals and current experience level
2. Recommend relevant Microsoft Learn resources and documentation
3. Create a structured learning path with:
   - Clear progression from basics to advanced
   - Estimated time for each section
   - Links to specific documentation and tutorials
   - Hands-on exercises where applicable

**For Coding Help Requests:**
When a user asks for code samples or coding assistance:
1. FIRST gather context about what they need
2. Identify relevant documentation and best practices
3. Then hand off to coding_agent with context about what they need
4. Call handoff_to_coding_agent and include a summary of the requirements

Example flow for coding requests:
- User: "Show me how to create an Azure Function"
- You: Acknowledge the request, note Azure Functions best practices
- You: Hand off to coding_agent with: "User needs an Azure Function example. Key points: HTTP trigger, Python, include error handling."

**Handoff to Coding Agent:**
When handing off to the coding agent, provide:
- Summary of what the user needs
- Any specific requirements mentioned
- Best practices to follow
- Language preference if mentioned

Be encouraging and adapt to the user's stated experience level!""",
        tools=[mcp_tool],
    )


def create_coding_agent(client: AzureOpenAIChatClient):
    """Create the Coding Agent - Code Generation Specialist."""
    return client.create_agent(
        name="coding-agent",
        instructions="""You are the Code Generation Specialist for the Developer Onboarding program.

You generate high-quality code samples to help new developers get started quickly.

**When you receive a handoff from the Learning Agent:**
The learning agent will provide you with context about:
- What the user needs
- Any specific requirements
- Best practices to follow

Use this context to generate the best possible code sample.

**Code Generation Guidelines:**
1. Write clean, well-documented code with comments
2. Include type hints (for Python) and proper typing
3. Follow language-specific best practices and conventions
4. Handle errors appropriately
5. Include usage examples in comments

**Code Output Format:**
- Start with a brief explanation of what the code does
- Provide the complete, runnable code
- Add inline comments explaining key parts
- End with usage instructions or next steps

**Supported Tasks:**
- Generate code snippets in any language (default to Python)
- Create Azure-specific code (Functions, CosmosDB, Storage, etc.)
- Write API integrations
- Create utility functions and helpers
- Build complete starter templates

**After Generating Code:**
- Explain any prerequisites or dependencies
- Suggest improvements or extensions
- Offer to modify the code based on feedback
- Ask if they need the code in a different language

Remember: You're helping new developers, so be clear and educational!""",
    )


def build_handoff_workflow(triage, employee_search, learning, coding):
    """Build the handoff workflow with routing rules."""
    workflow = (
        HandoffBuilder(
            name="developer_onboarding_workflow",
            participants=[triage, employee_search, learning, coding],
        )
        .set_coordinator(triage)
        .add_handoff(triage, [employee_search, learning, coding])
        .add_handoff(learning, [coding])
        .add_handoff(coding, [learning])
        .with_termination_condition(
            lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 20
        )
        .build()
    )
    return workflow


def main():
    """Main entry point for the hosted multi-agent workflow."""
    # Create Azure OpenAI client
    client = AzureOpenAIChatClient(credential=DefaultAzureCredential())

    # Create all specialized agents
    triage_agent = create_triage_agent(client)
    employee_search_agent = create_employee_search_agent(client)
    learning_agent = create_learning_agent(client)
    coding_agent = create_coding_agent(client)

    # Build the handoff workflow
    workflow = build_handoff_workflow(
        triage_agent,
        employee_search_agent,
        learning_agent,
        coding_agent,
    )

    # Convert the workflow to an agent and run as hosted agent
    # This exposes the workflow on localhost:8088 with Responses API compatibility
    workflow_agent = workflow.as_agent()
    from_agent_framework(workflow_agent).run()


if __name__ == "__main__":
    main()
```

**Multi-Agent Workflow Architecture:**

```
                    ┌─────────────────────────────────────┐
                    │          USER REQUEST               │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │          TRIAGE AGENT               │
                    │     (Coordinator/Router)            │
                    └─────────────────┬───────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│ EMPLOYEE SEARCH AGENT │ │    LEARNING AGENT     │ │    CODING AGENT       │
│  (File Search Tool)   │ │  (Microsoft Learn MCP)│ │  (Code Generation)    │
│                       │ │                       │ │                       │
│ - Org structure       │ │ - Learning paths      │ │ - Code samples        │
│ - Team info           │ │ - Documentation       │ │ - Azure integrations  │
│ - Colleague search    │ │ - Training plans      │ │ - Best practices      │
└───────────────────────┘ └───────────┬───────────┘ └───────────────────────┘
                                      │                         ▲
                                      └─────────────────────────┘
                                         (handoff for code)
```

**Key Features:**
- Full multi-agent orchestration using `HandoffBuilder` pattern
- Triage agent intelligently routes to specialists
- Employee search uses Azure AI File Search with vector store
- Learning agent integrates Microsoft Learn via MCP tool
- Coding agent generates production-ready code
- Agents can hand off to each other (learning → coding)

#### Step 2.2: Create Requirements File
**Status**: 🔲 Not Started

Create `hosted-agent/requirements.txt`:

```text
azure-ai-agentserver-agentframework==1.0.0b3
agent-framework
azure-identity
python-dotenv
```

#### Step 2.3: Create Dockerfile
**Status**: 🔲 Not Started

Create `hosted-agent/Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . user_agent/
WORKDIR /app/user_agent

RUN if [ -f requirements.txt ]; then \
        pip install -r requirements.txt; \
    else \
        echo "No requirements.txt found"; \
    fi

EXPOSE 8088

CMD ["python", "main.py"]
```

#### Step 2.4: Create Agent Definition YAML
**Status**: 🔲 Not Started

Create `hosted-agent/agent.yaml`:

```yaml
name: developer-onboarding-workflow
description: >
  A multi-agent developer onboarding workflow that helps new employees with:
  - Organizational questions via Employee Search Agent (file search)
  - Learning paths via Learning Agent (Microsoft Learn MCP)
  - Code generation via Coding Agent
  
  Uses HandoffBuilder pattern for intelligent routing between 4 specialized agents.
metadata:
  authors:
    - Microsoft Agent Framework Team
  tags:
    - Azure AI AgentServer
    - Microsoft Agent Framework
    - Multi-Agent Workflow
    - HandoffBuilder
    - Developer Onboarding
template:
  name: developer-onboarding-workflow
  kind: hosted
  protocols:
    - protocol: responses
  environment_variables:
    - name: AZURE_OPENAI_ENDPOINT
      value: ${AZURE_OPENAI_ENDPOINT}
    - name: AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
      value: "{{chat}}"
    - name: VECTOR_STORE_ID
      value: ${VECTOR_STORE_ID}
    - name: AZURE_AI_PROJECT_ENDPOINT
      value: ${AZURE_AI_PROJECT_ENDPOINT}
resources:
  - kind: model
    id: gpt-4o
    name: chat
```

---

### Phase 3: Deploy the Hosted Agent to Azure AI Foundry

#### Step 3.1: Build and Push Docker Image to ACR
**Status**: 🔲 Not Started

```bash
# Navigate to hosted agent directory
cd lesson-4-agentdeployment/hosted-agent

# Build Docker image
docker build -t developer-onboarding-agent:v1 .

# Login to Azure Container Registry
az acr login --name your-registry

# Tag image for ACR
docker tag developer-onboarding-agent:v1 your-registry.azurecr.io/developer-onboarding-agent:v1

# Push to ACR
docker push your-registry.azurecr.io/developer-onboarding-agent:v1
```

#### Step 3.2: Configure ACR Permissions
**Status**: 🔲 Not Started

Grant the Foundry project's managed identity access to ACR:

1. Go to Azure Portal → Your Foundry Project → Identity
2. Copy the Object (principal) ID
3. Go to ACR → Access Control (IAM)
4. Add role assignment: **Container Registry Repository Reader**
5. Assign to the Foundry project's managed identity

#### Step 3.3: Deploy Using Azure Developer CLI (Recommended)
**Status**: 🔲 Not Started

```bash
# Install/update azd
az upgrade

# Initialize with starter template (if starting fresh)
azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic

# Or initialize with existing Foundry project
azd ai agent init --project-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}

# Initialize agent from agent.yaml
azd ai agent init -m hosted-agent/agent.yaml

# Deploy the agent
azd up
```

#### Step 3.4: Alternative - Deploy Using Azure AI Projects SDK
**Status**: 🔲 Not Started

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

client = AIProjectClient(
    endpoint="https://your-project.services.ai.azure.com/api/projects/project-name",
    credential=DefaultAzureCredential()
)

agent = client.agents.create_version(
    agent_name="developer-onboarding-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/developer-onboarding-agent:v1",
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": "https://your-project.services.ai.azure.com/api/projects/project-name",
            "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": "gpt-4o",
        }
    )
)
print(f"Agent created: {agent.id}")
```

#### Step 3.5: Test Local Agent Before Deployment
**Status**: 🔲 Not Started

Test locally using the hosting adapter (runs on localhost:8088):

```bash
cd hosted-agent
python main.py
```

Test with REST call:
```http
POST http://localhost:8088/responses
Content-Type: application/json

{
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "Who works at the company?"
            }
        ]
    }
}
```

---

### Phase 4: Create the ChatKit Frontend and Server

#### Step 4.1: Implement ChatKit Server Backend
**Status**: 🔲 Not Started

Create `chatkit-server/app.py` - FastAPI server that calls the hosted multi-agent workflow:

```python
"""
ChatKit Server for Developer Onboarding Multi-Agent Workflow

This FastAPI server provides a ChatKit-compatible interface to interact with
the hosted multi-agent workflow on Azure AI Foundry. It handles:
- Thread management (create, list, load)
- Message persistence via SQLite
- Streaming responses from the hosted workflow agent
"""

import logging
import os
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

import uvicorn
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference
from azure.identity import AzureCliCredential
from chatkit.server import ChatKitServer
from chatkit.types import (
    ThreadItem,
    ThreadItemDoneEvent,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
    AssistantMessageItem,
    TextContent,
)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from store import SQLiteStore

# Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8001
DATABASE_PATH = "chatkit_onboarding.db"
HOSTED_AGENT_NAME = "developer-onboarding-workflow"
HOSTED_AGENT_VERSION = "1"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnboardingChatKitServer(ChatKitServer[dict[str, Any]]):
    """ChatKit server that communicates with the hosted multi-agent workflow."""

    def __init__(self, data_store: SQLiteStore):
        super().__init__(data_store)
        
        # Initialize Azure AI Project client
        self.project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=AzureCliCredential()
        )
        self.openai_client = self.project_client.get_openai_client()
        
        logger.info("OnboardingChatKitServer initialized")

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Handle incoming messages by routing to the hosted multi-agent workflow."""
        
        if input_user_message is None:
            return

        logger.info(f"Processing message for thread: {thread.id}")

        # Load thread history for context
        thread_items_page = await self.store.load_thread_items(
            thread_id=thread.id,
            after=None,
            limit=100,
            order="asc",
            context=context,
        )
        
        # Build conversation history for the hosted agent
        messages = []
        for item in thread_items_page.data:
            if isinstance(item, UserMessageItem) and item.content:
                for content_part in item.content:
                    if hasattr(content_part, "text"):
                        messages.append({"role": "user", "content": content_part.text})
            elif isinstance(item, AssistantMessageItem) and item.content:
                for content_part in item.content:
                    if hasattr(content_part, "text"):
                        messages.append({"role": "assistant", "content": content_part.text})

        # Add the current user message
        user_text = ""
        if input_user_message.content:
            for content_part in input_user_message.content:
                if hasattr(content_part, "text"):
                    user_text = content_part.text
                    break
        
        messages.append({"role": "user", "content": user_text})

        try:
            # Call the hosted multi-agent workflow via Responses API
            response = self.openai_client.responses.create(
                input=messages,
                stream=True,
                extra_body={
                    "agent": AgentReference(
                        name=HOSTED_AGENT_NAME,
                        version=HOSTED_AGENT_VERSION
                    ).as_dict()
                }
            )

            # Stream the response back to ChatKit
            full_response = ""
            for event in response:
                if hasattr(event, 'delta') and event.delta:
                    full_response += event.delta
                    # Could yield incremental updates here for streaming

            # Create the assistant message item
            item_id = f"msg_{datetime.now().timestamp()}"
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[TextContent(type="text", text=full_response)],
            )
            
            yield ThreadItemDoneEvent(type="thread.item.done", item=assistant_item)

            logger.info(f"Response completed for thread: {thread.id}")

        except Exception as e:
            logger.error(f"Error calling hosted agent: {e}", exc_info=True)
            # Return error message
            error_item = AssistantMessageItem(
                id=f"error_{datetime.now().timestamp()}",
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[TextContent(
                    type="text", 
                    text=f"Sorry, I encountered an error: {str(e)}"
                )],
            )
            yield ThreadItemDoneEvent(type="thread.item.done", item=error_item)


# FastAPI application
app = FastAPI(
    title="Developer Onboarding ChatKit Server",
    description="ChatKit interface for the multi-agent onboarding workflow",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize store and server
data_store = SQLiteStore(db_path=DATABASE_PATH)
chatkit_server = OnboardingChatKitServer(data_store)


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """Main ChatKit endpoint."""
    request_body = await request.body()
    context = {"request": request}
    
    result = await chatkit_server.process(request_body, context)
    
    if hasattr(result, "__aiter__"):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


if __name__ == "__main__":
    logger.info(f"Starting ChatKit server on {SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")
```

#### Step 4.2: Create SQLite Store Implementation

**Status**: 🔲 Not Started

Create `chatkit-server/store.py` - Complete persistence layer for ChatKit:

```python
"""
SQLite-based storage for ChatKit threads and messages.
"""

import json
import logging
import sqlite3
import uuid
from datetime import datetime
from typing import Any

from chatkit.types import (
    CreateThreadRequest,
    LoadThreadItemsResponse,
    LoadThreadsResponse,
    ListItemsCursor,
    ThreadItem,
    ThreadMetadata,
    UserMessageItem,
    AssistantMessageItem,
    TextContent,
)

logger = logging.getLogger(__name__)


class SQLiteStore:
    """SQLite-based storage implementing ChatKit Store protocol."""

    def __init__(self, db_path: str = "chatkit_onboarding.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Threads table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS threads (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    metadata TEXT
                )
            """)
            
            # Thread items (messages) table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thread_items (
                    id TEXT PRIMARY KEY,
                    thread_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_thread_items_thread_id 
                ON thread_items(thread_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_thread_items_created_at 
                ON thread_items(thread_id, created_at)
            """)
            
            conn.commit()
        logger.info(f"Database initialized at {self.db_path}")

    async def create_thread(
        self, request: CreateThreadRequest, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Create a new conversation thread."""
        thread_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        title = request.title if request.title else "New Conversation"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO threads (id, title, created_at, updated_at, metadata) VALUES (?, ?, ?, ?, ?)",
                (thread_id, title, now, now, json.dumps({}))
            )
            conn.commit()
        
        logger.info(f"Created thread: {thread_id}")
        return ThreadMetadata(
            id=thread_id,
            title=title,
            created_at=datetime.fromisoformat(now),
        )

    async def save_thread(
        self, thread: ThreadMetadata, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Save or update a thread."""
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE threads SET title = ?, updated_at = ? WHERE id = ?",
                (thread.title, now, thread.id)
            )
            conn.commit()
        
        return thread

    async def load_thread(
        self, thread_id: str, context: dict[str, Any]
    ) -> ThreadMetadata | None:
        """Load a thread by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, created_at, updated_at FROM threads WHERE id = ?",
                (thread_id,)
            )
            row = cursor.fetchone()
        
        if row is None:
            return None
        
        return ThreadMetadata(
            id=row[0],
            title=row[1],
            created_at=datetime.fromisoformat(row[2]),
        )

    async def load_threads(
        self, 
        after: str | None, 
        limit: int, 
        context: dict[str, Any]
    ) -> LoadThreadsResponse:
        """Load all threads with pagination."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if after:
                cursor.execute(
                    """SELECT id, title, created_at FROM threads 
                       WHERE created_at < (SELECT created_at FROM threads WHERE id = ?)
                       ORDER BY created_at DESC LIMIT ?""",
                    (after, limit + 1)
                )
            else:
                cursor.execute(
                    "SELECT id, title, created_at FROM threads ORDER BY created_at DESC LIMIT ?",
                    (limit + 1,)
                )
            
            rows = cursor.fetchall()
        
        has_more = len(rows) > limit
        threads = [
            ThreadMetadata(
                id=row[0],
                title=row[1],
                created_at=datetime.fromisoformat(row[2]),
            )
            for row in rows[:limit]
        ]
        
        next_cursor = threads[-1].id if has_more and threads else None
        
        return LoadThreadsResponse(
            data=threads,
            cursor=ListItemsCursor(next_cursor=next_cursor) if next_cursor else ListItemsCursor(),
        )

    async def delete_thread(self, thread_id: str, context: dict[str, Any]) -> None:
        """Delete a thread and all its messages."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM thread_items WHERE thread_id = ?", (thread_id,))
            cursor.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
            conn.commit()
        
        logger.info(f"Deleted thread: {thread_id}")

    async def save_thread_item(
        self, 
        thread_id: str, 
        item: ThreadItem, 
        context: dict[str, Any]
    ) -> ThreadItem:
        """Save a message to a thread."""
        now = datetime.now().isoformat()
        
        # Determine role and content
        role = "user" if isinstance(item, UserMessageItem) else "assistant"
        content_text = ""
        if item.content:
            for content_part in item.content:
                if hasattr(content_part, "text"):
                    content_text = content_part.text
                    break
        
        item_id = item.id if item.id else str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO thread_items 
                   (id, thread_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)""",
                (item_id, thread_id, role, content_text, now)
            )
            # Update thread's updated_at timestamp
            cursor.execute(
                "UPDATE threads SET updated_at = ? WHERE id = ?",
                (now, thread_id)
            )
            conn.commit()
        
        return item

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict[str, Any],
    ) -> LoadThreadItemsResponse:
        """Load messages from a thread."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            order_direction = "ASC" if order == "asc" else "DESC"
            
            if after:
                cursor.execute(
                    f"""SELECT id, role, content, created_at FROM thread_items 
                        WHERE thread_id = ? AND created_at > 
                            (SELECT created_at FROM thread_items WHERE id = ?)
                        ORDER BY created_at {order_direction} LIMIT ?""",
                    (thread_id, after, limit + 1)
                )
            else:
                cursor.execute(
                    f"""SELECT id, role, content, created_at FROM thread_items 
                        WHERE thread_id = ? ORDER BY created_at {order_direction} LIMIT ?""",
                    (thread_id, limit + 1)
                )
            
            rows = cursor.fetchall()
        
        has_more = len(rows) > limit
        items: list[ThreadItem] = []
        
        for row in rows[:limit]:
            item_id, role, content, created_at = row
            content_obj = [TextContent(type="text", text=content)]
            created_dt = datetime.fromisoformat(created_at)
            
            if role == "user":
                items.append(UserMessageItem(
                    id=item_id,
                    thread_id=thread_id,
                    created_at=created_dt,
                    content=content_obj,
                ))
            else:
                items.append(AssistantMessageItem(
                    id=item_id,
                    thread_id=thread_id,
                    created_at=created_dt,
                    content=content_obj,
                ))
        
        next_cursor = items[-1].id if has_more and items else None
        
        return LoadThreadItemsResponse(
            data=items,
            cursor=ListItemsCursor(next_cursor=next_cursor) if next_cursor else ListItemsCursor(),
        )

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: dict[str, Any]
    ) -> None:
        """Delete a specific message from a thread."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM thread_items WHERE id = ? AND thread_id = ?",
                (item_id, thread_id)
            )
            conn.commit()
```

#### Step 4.3: Create Frontend React Application

**Status**: 🔲 Not Started

Create `chatkit-server/frontend/` with ChatKit UI components:

**package.json:**

```json
{
  "name": "developer-onboarding-chatkit",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@openai/chatkit": "^0.1.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.5.0",
    "vite": "^5.4.0"
  }
}
```

**src/App.tsx:**

```tsx
import { ChatKitProvider, Chat, ThreadList, Header } from "@openai/chatkit";
import "./App.css";

export default function App() {
  return (
    <ChatKitProvider endpoint="http://localhost:8001/chatkit">
      <div className="app-container">
        <aside className="sidebar">
          <div className="sidebar-header">
            <h2>💼 Developer Onboarding</h2>
          </div>
          <ThreadList />
        </aside>
        <main className="main-content">
          <Header />
          <Chat
            placeholder="Ask me anything about onboarding, teammates, learning resources, or coding help..."
          />
        </main>
      </div>
    </ChatKitProvider>
  );
}
```

**src/App.css:**

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.app-container {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

.sidebar {
  width: 280px;
  background-color: #1a1a1a;
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #333;
}

.sidebar-header h2 {
  font-size: 1.1rem;
  font-weight: 600;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
}
```

**src/main.tsx:**

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**index.html:**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Developer Onboarding Assistant</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**vite.config.ts:**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/chatkit": {
        target: "http://localhost:8001",
        changeOrigin: true,
      },
    },
  },
});
```

---

### Phase 5: Run and Test the Complete Solution

#### Step 5.1: Start the Hosted Agent (or verify Azure deployment)

**Status**: 🔲 Not Started

**For Local Testing:**

```bash
cd hosted-agent
python main.py
# Multi-agent workflow runs on localhost:8088
```

**For Azure Deployed Agent:**

- Verify agent status in Azure AI Foundry portal
- Test via agent playground UI

#### Step 5.2: Start the ChatKit Backend Server

**Status**: 🔲 Not Started

```bash
cd chatkit-server
pip install -r requirements.txt
python app.py
# Server runs on localhost:8001
```

Or with auto-reload:

```bash
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

#### Step 5.3: Start the ChatKit Frontend

**Status**: 🔲 Not Started

```bash
cd chatkit-server/frontend
npm install
npm run dev
# Frontend runs on localhost:3000
```

#### Step 5.4: Access and Test the Application

**Status**: 🔲 Not Started

1. Open browser: `http://localhost:3000`
2. Test the multi-agent workflow with sample queries:

**Employee Search Agent Queries:**
- "I'm new here! Has anyone worked at Microsoft here?"
- "Who works at the company?"
- "Find employees with Azure experience"
- "Who has a background in data science?"

**Learning Agent Queries:**
- "Create a learning path for Azure Functions"
- "What resources do you recommend for learning Kubernetes?"
- "Build me a training plan for getting Azure certified"

**Coding Agent Queries:**
- "Help me write Python code for connecting to CosmosDB"
- "Create a sample Azure Function that processes HTTP requests"
- "Write a script to authenticate with Azure using managed identity"

**Multi-Agent Workflow Queries:**
- "I'm starting as a cloud engineer. Who should I connect with and what should I learn first?"
- "Find team members who work on AI projects and create a learning path for me to catch up"
- "I need to build an Azure Function - who has experience with this and can you show me sample code?"

---

### Phase 6: Optional Enhancements

#### Step 6.1: Add Observability with Application Insights

**Status**: 🔲 Not Started

- Enable OpenTelemetry tracing in the hosted agent
- Configure Application Insights connection string via environment variable
- View traces in Azure portal or AI Toolkit in VS Code

Example configuration in main.py:

```python
from azure.monitor.opentelemetry import configure_azure_monitor

# Add at start of main()
configure_azure_monitor(
    connection_string=os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
)
```

#### Step 6.2: Expand the Workflow with ConcurrentBuilder

**Status**: 🔲 Not Started

For parallel agent execution (e.g., searching employees AND learning resources simultaneously):

```python
from agent_framework import ConcurrentBuilder

# Create concurrent workflow for parallel queries
concurrent_workflow = (
    ConcurrentBuilder()
    .participants([employee_search_agent, learning_agent])
    .build()
)

# Use in combination with HandoffBuilder for hybrid workflows
```

#### Step 6.3: Add Custom ChatKit Widgets

**Status**: 🔲 Not Started

Implement custom ChatKit widgets for rich responses:

- Employee profile cards with photos
- Learning path progress indicators
- Code syntax highlighting with copy button
- File search results with document previews

---

## File Checklist

| File | Description | Status |
|------|-------------|--------|
| `hosted-agent/main.py` | Multi-agent workflow with HandoffBuilder | 🔲 |
| `hosted-agent/requirements.txt` | Python dependencies for agent framework | 🔲 |
| `hosted-agent/Dockerfile` | Container build file for Azure hosting | 🔲 |
| `hosted-agent/agent.yaml` | Agent definition for azd deployment | 🔲 |
| `chatkit-server/app.py` | FastAPI ChatKit server backend | 🔲 |
| `chatkit-server/store.py` | SQLite storage for threads/messages | 🔲 |
| `chatkit-server/requirements.txt` | Python dependencies for FastAPI server | 🔲 |
| `chatkit-server/frontend/package.json` | Node.js dependencies for React app | 🔲 |
| `chatkit-server/frontend/vite.config.ts` | Vite build configuration | 🔲 |
| `chatkit-server/frontend/src/App.tsx` | Main ChatKit UI component | 🔲 |
| `chatkit-server/frontend/src/App.css` | Styling for the chat interface | 🔲 |
| `chatkit-server/frontend/src/main.tsx` | React entry point | 🔲 |
| `chatkit-server/frontend/index.html` | HTML template | 🔲 |
| `.env.example` | Environment variables template | 🔲 |

---

## Reference Documentation

- [Azure AI Foundry Hosted Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/hosted-agents)
- [ChatKit Integration Sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/chatkit-integration)
- [Hosted Agents in Workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/demos/hosted_agents/agents_in_workflow)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/overview)

---

## Notes

1. **Region Availability**: Hosted agents are currently supported in **North Central US only** (more regions coming soon)
2. **Pricing**: Billing for managed hosting runtime will be enabled no earlier than February 1st, 2026 during preview
3. **Limits During Preview**:
   - Max 200 agents per Foundry resource
   - Max 2 min_replica count
   - Max 5 max_replica count
4. **Vector Store**: Ensure the vector store is created and populated before deploying the agent
5. **MCP Server**: The Microsoft Learn MCP server URL must be accessible from Azure

---

## Approval

Please review this implementation plan. Once approved, I will proceed with creating the files in the order specified above.

The implementation preserves the complete 4-agent workflow from the existing `agent-deployment.py`:

- **Triage Agent**: Coordinator that routes queries to specialists
- **Employee Search Agent**: Uses HostedFileSearchTool with vector store
- **Learning Agent**: Uses HostedMCPTool for Microsoft Learn resources  
- **Coding Agent**: Generates code samples and technical guidance

**Ready to proceed with file creation?**