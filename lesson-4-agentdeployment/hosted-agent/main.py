"""
Developer Onboarding Multi-Agent Workflow - Hosted Agent

This module implements a hosted agent for Azure AI Foundry that provides
a comprehensive developer onboarding experience using four specialized agents:

1. Triage Agent - Routes queries to appropriate specialists
2. Employee Search Agent - Finds colleagues using vector store
3. Learning Agent - Creates learning paths using Microsoft Learn
4. Coding Agent - Generates code samples and technical guidance

The agents are orchestrated using HandoffBuilder for intelligent routing.
"""

import os
import logging
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    HostedFileSearchTool,
    HostedMCPTool,
    HostedMCPToolParameters,
    HostedMCPConnection,
)
from azure.identity import DefaultAzureCredential
from agent_framework import HandoffBuilder
from azure.ai.agentserver.agentframework import from_agent_framework

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
AZURE_AI_PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")
MODEL_DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-4o")

# Initialize Azure AI Project client
client = AIProjectClient(
    endpoint=AZURE_AI_PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)


def create_file_search_tool() -> HostedFileSearchTool:
    """Create the file search tool for employee directory search."""
    return HostedFileSearchTool(
        vector_store_ids=[VECTOR_STORE_ID],
        max_num_results=5,
        include_search_results=True
    )


def create_mcp_tool() -> HostedMCPTool:
    """Create the MCP tool for Microsoft Learn integration."""
    return HostedMCPTool(
        parameters=HostedMCPToolParameters(
            connections=[
                HostedMCPConnection(
                    url="https://learn.microsoft.com/api/mcp",
                    display_name="Microsoft Learn"
                )
            ]
        )
    )


def create_agents():
    """
    Create all four specialized agents for the onboarding workflow.
    
    Returns:
        Tuple of (triage_agent, employee_search_agent, learning_agent, coding_agent)
    """
    # Create tools
    file_search_tool = create_file_search_tool()
    mcp_tool = create_mcp_tool()
    
    # Triage Agent - Coordinator
    triage_agent = client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="triage-agent",
        instructions="""You are the triage agent for the Developer Onboarding System.
Your role is to understand what the new developer needs and route them to the appropriate specialist:

1. **Employee Search Agent**: For questions about finding colleagues, team members, 
   who works on what, or connecting with people.
   
2. **Learning Agent**: For questions about training resources, learning paths, 
   certifications, documentation, or skill development.
   
3. **Coding Agent**: For questions about code examples, technical implementation,
   best practices, or help writing code.

Always be welcoming and helpful. When routing, briefly explain why you're 
connecting them with a particular specialist.

If the request spans multiple areas, start with the most relevant specialist 
and let them know you can help with other aspects afterward."""
    )
    logger.info(f"Created triage agent: {triage_agent.id}")
    
    # Employee Search Agent
    employee_search_agent = client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="employee-search-agent",
        instructions="""You are the Employee Search Agent for the Developer Onboarding System.
You help new developers find and connect with colleagues.

Your capabilities:
- Search the employee directory using the file search tool
- Find people by name, skills, department, or experience
- Provide relevant background information about colleagues
- Suggest people to connect with based on the new hire's interests

When presenting search results:
- Format employee information clearly
- Highlight relevant skills and experience
- Suggest why connecting with each person might be valuable
- Offer to search for more specific criteria if needed

Always be helpful and facilitate connections within the organization.""",
        tools=[file_search_tool]
    )
    logger.info(f"Created employee search agent: {employee_search_agent.id}")
    
    # Learning Agent
    learning_agent = client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="learning-agent",
        instructions="""You are the Learning Agent for the Developer Onboarding System.
You help new developers create personalized learning paths and find training resources.

Your capabilities:
- Access Microsoft Learn documentation and tutorials via MCP
- Create customized learning paths based on role and goals
- Recommend certifications and training programs
- Find documentation for specific technologies

When creating learning paths:
- Consider the developer's current skill level
- Prioritize foundational knowledge before advanced topics
- Include hands-on labs and practical exercises
- Estimate time requirements for each resource
- Suggest certifications that align with their goals

Always provide structured, actionable learning recommendations.""",
        tools=[mcp_tool]
    )
    logger.info(f"Created learning agent: {learning_agent.id}")
    
    # Coding Agent
    coding_agent = client.agents.create_agent(
        model=MODEL_DEPLOYMENT,
        name="coding-agent",
        instructions="""You are the Coding Agent for the Developer Onboarding System.
You help new developers with code examples, technical implementation, and best practices.

Your capabilities:
- Generate code samples in multiple languages (Python, C#, JavaScript, etc.)
- Explain coding patterns and best practices
- Help debug and troubleshoot code issues
- Provide Azure-specific code examples and SDK usage

When providing code:
- Write clean, well-commented code
- Follow language-specific best practices
- Include error handling where appropriate
- Explain key concepts and design decisions
- Suggest improvements and alternatives when relevant

Focus on practical, production-ready code examples that follow 
Microsoft/Azure best practices."""
    )
    logger.info(f"Created coding agent: {coding_agent.id}")
    
    return triage_agent, employee_search_agent, learning_agent, coding_agent


def build_handoff_workflow(triage, employee_search, learning, coding):
    """
    Build the multi-agent workflow using HandoffBuilder.
    
    The workflow uses triage as the coordinator that can hand off to specialists.
    Specialists can also hand off to each other for related queries.
    
    Args:
        triage: The triage (coordinator) agent
        employee_search: The employee search specialist agent
        learning: The learning path specialist agent
        coding: The coding specialist agent
        
    Returns:
        Built workflow object
    """
    workflow = (
        HandoffBuilder(
            name="developer-onboarding-workflow",
            description="Multi-agent system for developer onboarding support"
        )
        # Set triage as the coordinator - receives all initial queries
        .set_coordinator(triage)
        
        # Define handoff rules from triage to specialists
        .add_handoff(
            source=triage,
            targets=[employee_search, learning, coding],
            description="Route to appropriate specialist based on query type"
        )
        
        # Allow specialists to hand off to each other for related queries
        .add_handoff(
            source=employee_search,
            targets=[learning, coding],
            description="Hand off to learning for training or coding for technical help"
        )
        .add_handoff(
            source=learning,
            targets=[employee_search, coding],
            description="Hand off to employee search for mentors or coding for implementation"
        )
        .add_handoff(
            source=coding,
            targets=[employee_search, learning],
            description="Hand off to employee search for experts or learning for documentation"
        )
        
        # All specialists can return to triage for new topics
        .add_handoff(
            source=employee_search,
            targets=[triage],
            description="Return to triage for unrelated queries"
        )
        .add_handoff(
            source=learning,
            targets=[triage],
            description="Return to triage for unrelated queries"
        )
        .add_handoff(
            source=coding,
            targets=[triage],
            description="Return to triage for unrelated queries"
        )
        
        # Configure termination conditions
        .with_termination_condition(
            max_turns=20,
            end_on_no_handoff=True
        )
        
        # Build the workflow
        .build()
    )
    
    logger.info("Built handoff workflow successfully")
    return workflow


def main():
    """
    Main entry point for the hosted agent.
    
    Creates the multi-agent workflow and runs it as a hosted agent
    on Azure AI Foundry.
    """
    logger.info("Starting Developer Onboarding Hosted Agent...")
    logger.info(f"Project Endpoint: {AZURE_AI_PROJECT_ENDPOINT}")
    logger.info(f"Vector Store ID: {VECTOR_STORE_ID}")
    logger.info(f"Model Deployment: {MODEL_DEPLOYMENT}")
    
    # Create all agents
    triage, employee_search, learning, coding = create_agents()
    logger.info("All agents created successfully")
    
    # Build the handoff workflow
    workflow = build_handoff_workflow(triage, employee_search, learning, coding)
    
    # Convert workflow to a single agent interface
    workflow_agent = workflow.as_agent()
    logger.info("Workflow converted to agent interface")
    
    # Run as hosted agent on Azure AI Foundry
    # This starts the agent server on port 8088
    logger.info("Starting hosted agent server on port 8088...")
    from_agent_framework(workflow_agent).run()


if __name__ == "__main__":
    main()
