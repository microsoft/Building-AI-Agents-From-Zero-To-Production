"""
Azure Learning Agent - Uses Microsoft Learn MCP Server with AzureAIClient and DevUI

This agent helps developers create personalized learning plans based on their
interests and goals. It uses the HostedMCPTool pattern with AzureAIClient
which handles MCP connections server-side through Azure AI Agent Service.

Prerequisites:
1. Ensure you have Azure CLI credentials configured (run `az login`)

Usage:
    python azure-learning-agent.py
    
Then open http://localhost:8092 in your browser.
"""

import logging

from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

from agent_framework import HostedMCPTool
from agent_framework.azure import AzureAIClient

# Enable logging to see tool calls
logging.basicConfig(level=logging.INFO)
logging.getLogger("agent_framework").setLevel(logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

# Agent instructions
AGENT_INSTRUCTIONS = """You are a learning path assistant that helps developers create personalized training plans using Microsoft Learn documentation. ALWAYS use the Microsoft Learn MCP tool to search for relevant content.

When a user asks about learning something or creating a training plan, follow these steps:

1. **Understand Their Goals**: Ask the user about:
   - What topic or technology do they want to learn? (e.g., Azure, AI, Python, .NET, etc.)
   - What is their current experience level? (beginner/intermediate/advanced)
   - How much time do they have to dedicate to learning?
   - Any specific goals? (certification, job skill, project requirement)

2. **Research Content**: Use the Microsoft Learn MCP tools to search for relevant documentation, tutorials, and learning paths. Make multiple queries if needed to cover different aspects of the topic.

3. **Create a Learning Path**: Based on the search results and user's goals, create a structured learning plan with:
   - A clear progression from basics to advanced topics
   - Estimated time for each section
   - Links to specific Microsoft Learn articles and modules
   - Hands-on exercises or projects where applicable

4. **Provide the Plan**: Present the learning path in a clear, organized format:
   - Week-by-week or phase-by-phase breakdown
   - Prerequisites for each section
   - Key concepts they'll learn
   - Direct links to Microsoft Learn resources

Be encouraging and adapt the plan to the user's stated experience level and time constraints."""

# Create credential and client
credential = AzureCliCredential()
client = AzureAIClient(async_credential=credential)

# Create agent using the client's create_agent method with HostedMCPTool
# The MCP connection is handled server-side by Azure AI Agent Service
agent = client.create_agent(
    name="LearningPathAgent",
    instructions=AGENT_INSTRUCTIONS,
    tools=HostedMCPTool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
        approval_mode="never_require",
    ),
)

if __name__ == "__main__":
    from agent_framework.devui import serve

    print("Starting DevUI server at http://localhost:8092")
    serve(entities=[agent], port=8092)
