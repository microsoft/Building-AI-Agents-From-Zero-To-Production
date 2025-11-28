"""
Employee Search Agent - Uses HostedFileSearchTool with DevUI

Prerequisites:
1. Run setup_vector_store.py first to create the vector store
2. Copy the VECTOR_STORE_ID to your .env file

Usage:
    python employee-search-agent.py
    
Then open http://localhost:8090 in your browser.
"""

import os

from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

from agent_framework import ChatAgent, HostedFileSearchTool, HostedVectorStoreContent
from agent_framework.azure import AzureAIAgentClient

load_dotenv()

# Create the file search tool with pre-created vector store
file_search_tool = HostedFileSearchTool(
    inputs=[
        HostedVectorStoreContent(
            vector_store_id=os.environ["VECTOR_STORE_ID"]
        )
    ]
)

# Create the agent
agent = ChatAgent(
    chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
    instructions="""You are an employee search assistant for Zava, a software company.

Use the file search tool to find information about employees when asked questions like:
- "Is there anyone from my former company here?" (Note: The current user is "New Employee" who came from LinkedIn)
- "Who was the most recent joiner before me?"
- "Who is the manager for the AI Engineering Team?"
- "List all employees from Microsoft"
- "Who works on the Platform team?"

When answering questions about "my former company", remember that you are helping "New Employee" 
who previously worked at LinkedIn. Search for employees who also came from LinkedIn.

Always provide helpful, detailed responses based on the employee data.""",
    tools=[file_search_tool],
)

if __name__ == "__main__":
    from agent_framework.devui import serve

    serve(entities=[agent], port=8090)
