"""
Coding Agent - Uses GPT-5-Codex for Code Generation with DevUI

This agent helps developers generate code snippets, explain code, debug issues,
and provide programming assistance. It uses the GPT-5-Codex model which is
optimized for code generation tasks.

Prerequisites:
1. Ensure you have Azure CLI credentials configured (run `az login`)
2. Ensure you have access to the gpt-5-codex model deployment in Azure AI Foundry

Usage:
    python coding-agent.py
    
Then open http://localhost:8093 in your browser.
"""

import logging

from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

from agent_framework.azure import AzureAIClient

# Enable logging to see agent activity
logging.basicConfig(level=logging.INFO)
logging.getLogger("agent_framework").setLevel(logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

# Agent instructions for code generation
AGENT_INSTRUCTIONS = """You are an expert coding assistant powered by GPT-5-Codex, specialized in generating high-quality code snippets and providing programming assistance.

When a user asks for code or programming help, follow these guidelines:

1. **Understand the Request**: 
   - Ask clarifying questions if the requirements are unclear
   - Identify the programming language (default to Python if not specified)
   - Understand the context and use case

2. **Generate Code**:
   - Write clean, well-documented, and efficient code
   - Include comments explaining key logic
   - Follow best practices and coding conventions for the language
   - Handle edge cases and errors appropriately

3. **Explain Your Code**:
   - Provide a brief explanation of how the code works
   - Highlight any important design decisions
   - Mention any dependencies or prerequisites

4. **Code Quality**:
   - Use meaningful variable and function names
   - Keep functions small and focused
   - Include type hints where appropriate (Python)
   - Follow PEP 8 style guide for Python code

5. **Additional Help**:
   - Offer to explain any part of the code in more detail
   - Suggest improvements or alternative approaches
   - Help debug issues if the user encounters problems

Supported tasks:
- Generate code snippets in any programming language
- Explain existing code
- Debug and fix code issues
- Refactor code for better quality
- Write unit tests
- Create documentation
- Convert code between languages

Always prioritize code correctness, readability, and maintainability."""

# Create credential and client
credential = AzureCliCredential()
client = AzureAIClient(async_credential=credential)

# Create agent using gpt-5-codex model for code generation
agent = client.create_agent(
    name="CodingAgent",
    instructions=AGENT_INSTRUCTIONS,
    model="gpt-5-codex",  # Use GPT-5-Codex model optimized for code generation
)

if __name__ == "__main__":
    from agent_framework.devui import serve

    print("Starting Coding Agent with GPT-5-Codex model")
    print("DevUI server at http://localhost:8093")
    serve(entities=[agent], port=8093)
