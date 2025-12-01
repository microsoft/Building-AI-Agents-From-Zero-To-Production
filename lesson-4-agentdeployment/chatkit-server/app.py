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
SERVER_HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "8001"))
DATABASE_PATH = os.environ.get("DATABASE_PATH", "chatkit_onboarding.db")
HOSTED_AGENT_NAME = os.environ.get("HOSTED_AGENT_NAME", "developer-onboarding-workflow")
HOSTED_AGENT_VERSION = os.environ.get("HOSTED_AGENT_VERSION", "1")

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
        logger.info(f"Hosted Agent: {HOSTED_AGENT_NAME} v{HOSTED_AGENT_VERSION}")

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
        logger.info(f"Sending {len(messages)} messages to hosted agent")

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
                    # Could yield incremental updates here for real-time streaming

            # Create the assistant message item
            item_id = f"msg_{datetime.now().timestamp()}"
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[TextContent(type="text", text=full_response)],
            )
            
            # Save the assistant response to the store
            await self.store.save_thread_item(thread.id, assistant_item, context)
            
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
                    text=f"Sorry, I encountered an error processing your request. Please try again. Error: {str(e)}"
                )],
            )
            yield ThreadItemDoneEvent(type="thread.item.done", item=error_item)


# FastAPI application
app = FastAPI(
    title="Developer Onboarding ChatKit Server",
    description="ChatKit interface for the multi-agent onboarding workflow hosted on Azure AI Foundry",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize store and server (lazy initialization)
data_store: SQLiteStore | None = None
chatkit_server: OnboardingChatKitServer | None = None


def get_chatkit_server() -> OnboardingChatKitServer:
    """Get or create the ChatKit server instance."""
    global data_store, chatkit_server
    if chatkit_server is None:
        data_store = SQLiteStore(db_path=DATABASE_PATH)
        chatkit_server = OnboardingChatKitServer(data_store)
    return chatkit_server


@app.on_event("startup")
async def startup_event():
    """Initialize the ChatKit server on startup."""
    logger.info("Starting ChatKit server...")
    get_chatkit_server()
    logger.info("ChatKit server initialized")


@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "Developer Onboarding ChatKit Server",
        "version": "1.0.0",
        "hosted_agent": HOSTED_AGENT_NAME,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """Main ChatKit endpoint - handles all ChatKit protocol messages."""
    server = get_chatkit_server()
    request_body = await request.body()
    context = {"request": request}
    
    result = await server.process(request_body, context)
    
    if hasattr(result, "__aiter__"):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")


if __name__ == "__main__":
    logger.info(f"Starting ChatKit server on {SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")
