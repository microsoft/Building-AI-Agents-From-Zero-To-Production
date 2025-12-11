# Copyright (c) Microsoft. All rights reserved.

import os

from agent_framework import HostedMCPTool, HostedFileSearchTool, HostedVectorStoreContent
from agent_framework.azure import AzureOpenAIChatClient
# pyright: ignore[reportUnknownVariableType]
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity import DefaultAzureCredential

# Get vector store ID from environment
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")


def main():
    # Create the file search tool for employee directory
    file_search_tool = HostedFileSearchTool(
        inputs=[
            HostedVectorStoreContent(
                vector_store_id=VECTOR_STORE_ID
            )
        ]
    )

    # Create a single Developer Onboarding Agent with MCP and File Search tools
    agent = AzureOpenAIChatClient(credential=DefaultAzureCredential()).create_agent(
        name="DevOnboardingAgent",
        instructions="""You are a comprehensive Developer Onboarding Assistant. You help new developers with three key areas:

## 1. Employee Search & Connections
Use the file search tool to find information about employees when asked questions like:
- "Who should I connect with about [topic]?"
- "Who works on the [team name] team?"
- "Find colleagues with experience in [technology]"
- "Who is the manager for [team]?"
- "List employees who came from [company]"

When searching for employees, provide helpful details about their role, team, and expertise.

## 2. Learning & Training
Use the Microsoft Learn MCP tool for:
- Finding training resources and learning paths
- Creating customized learning paths based on role and goals
- Recommending certifications and training programs
- Finding documentation for specific technologies
- Prioritizing foundational knowledge before advanced topics

## 3. Coding Assistance
- Generate code samples in multiple languages (Python, C#, JavaScript, etc.)
- Explain coding patterns and best practices
- Help debug and troubleshoot code issues
- Provide Azure-specific code examples and SDK usage
- Write clean, well-commented, production-ready code

Always be welcoming, helpful, and provide actionable recommendations.""",
        tools=[
            file_search_tool,
            HostedMCPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
            ),
        ],
    )

    # Run the agent as a hosted agent
    from_agent_framework(agent).run()


if __name__ == "__main__":
    main()
