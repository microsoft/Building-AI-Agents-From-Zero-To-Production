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
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference
from chatkit.server import ChatKitServer
from chatkit.types import (
    AssistantMessageItem,
    ThreadItemDoneEvent,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
)
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse

from store import SQLiteStore

# ============================================================================
# Configuration Constants
# ============================================================================

# Server configuration
SERVER_HOST = os.environ.get("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "8001"))

# Database configuration
DATABASE_PATH = os.environ.get("DATABASE_PATH", "chatkit_onboarding.db")

# Azure AI Foundry Project configuration
PROJECT_ENDPOINT = os.environ.get(
    "PROJECT_ENDPOINT",
    "https://koreyst-3816-resource.services.ai.azure.com/api/projects/koreyst-3816"
)
AGENT_NAME = os.environ.get("AGENT_NAME", "agent-with-hosted-mcp")
AGENT_VERSION = os.environ.get("AGENT_VERSION", "1")

# User context
DEFAULT_USER_ID = "demo_user"

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# Logging Setup
# ============================================================================

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
)
logger = logging.getLogger(__name__)


class OnboardingChatKitServer(ChatKitServer[dict[str, Any]]):
    """ChatKit server that communicates with the hosted multi-agent workflow.
    
    This server integrates with a hosted agent on Azure AI Foundry using
    AIProjectClient and AgentReference for proper authentication.
    """

    def __init__(self, data_store: SQLiteStore):
        super().__init__(data_store)
        
        logger.info("Initializing OnboardingChatKitServer")
        
        # Initialize Azure AI Project client
        self.credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=self.credential
        )
        
        # Retrieve the agent
        logger.info(f"Retrieving agent: {AGENT_NAME}")
        self.agent = self.client.agents.get(agent_name=AGENT_NAME)
        logger.info(f"Agent retrieved: {self.agent.name}")
        
        # Get the OpenAI client for making requests
        self.openai_client = self.client.get_openai_client()
        
        logger.info(f"Project Endpoint: {PROJECT_ENDPOINT}")
        logger.info(f"Agent: {AGENT_NAME} (version {AGENT_VERSION})")
        logger.info("OnboardingChatKitServer initialized")

    def _call_agent(self, messages: list[dict[str, str]]) -> str:
        """Call the hosted agent and get the response.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            
        Returns:
            The agent's response text.
        """
        # Convert messages to the format expected by the OpenAI responses API
        input_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]
        
        logger.debug(f"Calling agent with {len(input_messages)} messages")
        
        # Call the agent using the OpenAI responses API
        response = self.openai_client.responses.create(
            input=input_messages,
            extra_body={
                "agent": AgentReference(
                    name=self.agent.name,
                    version=AGENT_VERSION
                ).as_dict()
            }
        )
        
        # Debug: log the full response structure
        logger.debug(f"Response type: {type(response)}")
        logger.debug(f"Response attributes: {dir(response)}")
        
        # Try to extract the text from various possible locations
        output_text = ""
        
        # Try output_text first (common for responses API)
        if hasattr(response, 'output_text') and response.output_text:
            output_text = response.output_text
            logger.debug(f"Found output_text: {output_text[:100] if output_text else 'empty'}...")
        # Try output array (responses API format)
        elif hasattr(response, 'output') and response.output:
            logger.debug(f"Response output: {response.output}")
            for item in response.output:
                if hasattr(item, 'content'):
                    for content_item in item.content:
                        if hasattr(content_item, 'text'):
                            output_text += content_item.text
                elif hasattr(item, 'text'):
                    output_text += item.text
        # Try choices (chat completions format)
        elif hasattr(response, 'choices') and response.choices:
            logger.debug(f"Response choices: {response.choices}")
            for choice in response.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    output_text += choice.message.content or ""
        
        # Log raw response for debugging if still empty
        if not output_text:
            logger.warning(f"Could not extract text. Raw response: {response}")
            # Try to convert to dict for inspection
            if hasattr(response, 'model_dump'):
                logger.warning(f"Response dict: {response.model_dump()}")
            elif hasattr(response, '__dict__'):
                logger.warning(f"Response __dict__: {response.__dict__}")
        
        return output_text

    async def _update_thread_title(
        self, 
        thread: ThreadMetadata, 
        user_message: str,
        context: dict[str, Any]
    ) -> None:
        """Update thread title based on first user message.
        
        Args:
            thread: The thread metadata to update.
            user_message: The user's message text.
            context: The context dictionary.
        """
        if not user_message:
            return
            
        # Simple truncation for title
        title = user_message[:50].strip()
        if len(user_message) > 50:
            title += "..."
            
        thread.title = title
        await self.store.save_thread(thread, context)
        logger.info(f"Updated thread {thread.id} title to: {title}")

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Handle incoming user messages and generate responses.
        
        This method loads thread history, calls the hosted agent,
        and streams the response back to ChatKit.
        """
        if input_user_message is None:
            logger.debug("Received None user message, skipping")
            return

        logger.info(f"Processing message for thread: {thread.id}")

        try:
            # Extract user message text
            user_text = ""
            if input_user_message.content:
                for content_part in input_user_message.content:
                    if hasattr(content_part, "text"):
                        user_text = content_part.text
                        break

            if not user_text:
                logger.warning("No text content in user message")
                return

            # Load thread history for context
            thread_items_page = await self.store.load_thread_items(
                thread_id=thread.id,
                after=None,
                limit=100,
                order="asc",
                context=context,
            )

            # Build conversation history for the hosted agent
            messages: list[dict[str, str]] = []
            
            # Add conversation history (the agent has its own system prompt)
            for item in thread_items_page.data:
                if isinstance(item, UserMessageItem) and item.content:
                    for content_part in item.content:
                        if hasattr(content_part, "text"):
                            messages.append({"role": "user", "content": content_part.text})
                            break
                elif isinstance(item, AssistantMessageItem) and item.content:
                    for content_part in item.content:
                        if hasattr(content_part, "text"):
                            messages.append({"role": "assistant", "content": content_part.text})
                            break

            # Add the current user message
            messages.append({"role": "user", "content": user_text})
            
            logger.info(f"Sending {len(messages)} messages to hosted agent")

            # Call the hosted agent
            full_response = ""
            
            try:
                full_response = self._call_agent(messages)
                logger.info(f"Received response from agent: {len(full_response)} chars")
                    
            except Exception as e:
                logger.error(f"Error calling hosted agent: {e}", exc_info=True)
                full_response = (
                    f"Sorry, I encountered an error processing your request. "
                    f"Please try again. Error: {str(e)}"
                )

            # Create the assistant message item
            item_id = f"msg_{datetime.now().timestamp()}"
            assistant_item = AssistantMessageItem(
                id=item_id,
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[{"type": "output_text", "text": full_response}],
            )

            # Yield the completed message event
            yield ThreadItemDoneEvent(type="thread.item.done", item=assistant_item)

            # Update thread title if it's a new conversation
            if not thread.title or thread.title == "New thread":
                await self._update_thread_title(thread, user_text, context)

            logger.info(f"Completed processing message for thread: {thread.id}")

        except Exception as e:
            logger.error(f"Error processing message for thread {thread.id}: {e}", exc_info=True)
            
            # Return error message to user
            error_item = AssistantMessageItem(
                id=f"error_{datetime.now().timestamp()}",
                thread_id=thread.id,
                created_at=datetime.now(),
                content=[{
                    "type": "output_text",
                    "text": f"Sorry, I encountered an error. Please try again. Error: {str(e)}"
                }],
            )
            yield ThreadItemDoneEvent(type="thread.item.done", item=error_item)


# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="Developer Onboarding ChatKit Server",
    description="ChatKit interface for the multi-agent onboarding workflow hosted on Azure AI Foundry",
    version="1.0.0",
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data store and ChatKit server
logger.info("Initializing application components")
data_store = SQLiteStore(db_path=DATABASE_PATH)
chatkit_server = OnboardingChatKitServer(data_store)
logger.info("Application initialization complete")


@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "Developer Onboarding ChatKit Server",
        "version": "1.0.0",
        "project_endpoint": PROJECT_ENDPOINT,
        "agent_name": AGENT_NAME,
        "agent_version": AGENT_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    """Main ChatKit endpoint that handles all ChatKit requests.
    
    This endpoint follows the ChatKit server protocol and handles both
    streaming and non-streaming responses.
    """
    logger.debug(f"Received ChatKit request from {request.client}")
    request_body = await request.body()

    # Create context with user ID
    context = {"request": request, "user_id": DEFAULT_USER_ID}

    try:
        # Process the request using ChatKit server
        result = await chatkit_server.process(request_body, context)

        # Return appropriate response type
        if hasattr(result, "__aiter__"):  # StreamingResult
            logger.debug("Returning streaming response")
            return StreamingResponse(result, media_type="text/event-stream")
        # NonStreamingResult
        logger.debug("Returning non-streaming response")
        return Response(content=result.json, media_type="application/json")
    except Exception as e:
        logger.error(f"Error processing ChatKit request: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Run the server
    logger.info(f"Starting ChatKit Developer Onboarding server on {SERVER_HOST}:{SERVER_PORT}")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, log_level="info")
