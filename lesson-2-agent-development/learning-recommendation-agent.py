"""
Learning Path Agent - Uses Microsoft Learn MCP Server with DevUI

This agent helps developers create personalized learning plans based on their
interests and goals. When a user asks about learning something, the agent will:
1. Ask about their learning goals and current experience level
2. Query Microsoft Learn documentation for relevant content
3. Create a structured learning path with recommended resources

Prerequisites:
1. Ensure you have Azure CLI credentials configured (run `az login`)

Usage:
    python learning-recommendation-agent.py
    
Then open http://localhost:8091 in your browser.
"""

import asyncio

from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient

# Load environment variables from .env file
load_dotenv()

# Agent instructions
AGENT_INSTRUCTIONS = """You are a learning path assistant that helps developers create personalized training plans using Microsoft Learn documentation.

When a user asks about learning something or creating a training plan, follow these steps:

1. **Understand Their Goals**: Ask the user about:
   - What topic or technology do they want to learn? (e.g., Azure, AI, Python, .NET, etc.)
   - What is their current experience level? (beginner/intermediate/advanced)
   - How much time do they have to dedicate to learning?
   - Any specific goals? (certification, job skill, project requirement)

2. **Research Content**: Use the Microsoft Learn MCP tools to search for relevant documentation:
   - Use microsoft_docs_search to find relevant articles and learning paths
   - Use microsoft_code_sample_search to find code examples
   - Use microsoft_docs_fetch to get full content of specific articles

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


# Create the Microsoft Learn MCP tool
learn_mcp_tool = MCPStreamableHTTPTool(
    name="Microsoft Learn MCP",
    url="https://learn.microsoft.com/api/mcp",
)

# Connect to MCP server (must be done before creating agent)
asyncio.get_event_loop().run_until_complete(learn_mcp_tool.connect())
print("Connected to Microsoft Learn MCP Server!")
print(f"Available tools: {[f.name for f in learn_mcp_tool.functions]}")

# Create the agent with the connected MCP tool
agent = ChatAgent(
    chat_client=AzureAIAgentClient(async_credential=AzureCliCredential()),
    name="LearningPathAgent",
    instructions=AGENT_INSTRUCTIONS,
    tools=learn_mcp_tool,
)

if __name__ == "__main__":
    from agent_framework.devui import serve

    print("\nStarting DevUI server at http://localhost:8091")
    serve(entities=[agent], port=8091)
