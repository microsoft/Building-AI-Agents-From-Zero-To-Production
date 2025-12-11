"""
Agent Orchestration - Developer Onboarding Assistant using Handoff Pattern

This application helps new developers onboard to a company by orchestrating
multiple specialized agents using the Microsoft Agent Framework's handoff pattern.

Routing Scenarios:
1. Organizational Questions → Employee Search Agent (search employee data)
2. Training Materials → Learning Agent (create learning paths)
3. Coding Help → Learning Agent (pulls docs) → Coding Agent (generates code)

The triage agent acts as the coordinator, routing requests to the appropriate
specialist agent based on the user's needs.

Prerequisites:
1. Ensure you have Azure CLI credentials configured (run `az login`)
2. Azure AI Project endpoint configured in environment variables:
   - AZURE_AI_PROJECT_ENDPOINT
   - VECTOR_STORE_ID

Usage:
    python agent-orchestration.py
    
Then open http://localhost:8094 in your browser.
"""

import logging
import os

from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

from agent_framework import (
    HandoffBuilder,
    HostedFileSearchTool,
    HostedMCPTool,
    HostedVectorStoreContent,
)
from agent_framework.azure import AzureAIClient

# Enable logging to see orchestration activity
logging.basicConfig(level=logging.INFO)
logging.getLogger("agent_framework").setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()

# Create credential at module level (same pattern as coding-agent.py)
credential = AzureCliCredential()

# Create separate client for each agent
triage_client = AzureAIClient(async_credential=credential)
employee_client = AzureAIClient(async_credential=credential)
learning_client = AzureAIClient(async_credential=credential)
coding_client = AzureAIClient(async_credential=credential)

# TRIAGE AGENT - The Coordinator
triage_agent = triage_client.create_agent(
    id="triage-agent",
    name="triage-agent",
    instructions="""You are the Developer Onboarding Assistant - a friendly coordinator helping new developers get settled at their new company.

Your role is to understand what the new developer needs and route them to the right specialist:

1. **Organizational Questions** -> Hand off to employee_search_agent
   - Questions about coworkers, teams, managers
   - Finding people from the same former company
   - Understanding the org structure
   - Examples: "Who is on my team?", "Is anyone else from my former company here?", "Who manages the AI team?"

2. **Training & Learning** -> Hand off to learning_agent
   - Creating learning paths and training plans
   - Finding documentation and tutorials
   - Understanding technologies used at the company
   - Examples: "I need to learn Azure", "Create a training plan for Python", "What should I learn first?"

3. **Coding Help & Code Samples** -> Hand off to learning_agent FIRST
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

# EMPLOYEE SEARCH AGENT - Organizational Knowledge Specialist
file_search_tool = HostedFileSearchTool(
    inputs=[
        HostedVectorStoreContent(
            vector_store_id=os.environ["VECTOR_STORE_ID"]
        )
    ]
)

employee_search_agent = employee_client.create_agent(
    id="employee-search-agent",
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

# LEARNING AGENT - Training & Documentation Specialist
mcp_tool = HostedMCPTool(
    name="Microsoft Learn MCP",
    url="https://learn.microsoft.com/api/mcp",
    approval_mode="never_require",
)

learning_agent = learning_client.create_agent(
    id="learning-agent",
    name="learning-agent",
    instructions="""You are the Learning Path Specialist for the Developer Onboarding program.

Use the Microsoft Learn MCP tool to find relevant documentation and learning resources.

**For Training/Documentation Requests (NO code needed):**
1. Understand their learning goals and current experience level
2. Use the MCP tool to find relevant Microsoft Learn resources
3. Create a structured learning path with clear progression
4. RESPOND DIRECTLY to the user - no handoff needed

**For Coding Help Requests:**
When a user asks for code samples or coding assistance:
1. FIRST use the MCP tool to gather ALL relevant documentation and best practices
2. Compile a COMPLETE context summary with everything the coding agent needs:
   - Correct Product Names
   - Exact user request (be specific)
   - Language preference (default: Python)  
   - Key best practices and patterns from documentation
   - Relevant API signatures, parameters, and examples
   - Any configuration or setup requirements
3. Hand off to coding_agent with this complete context

**IMPORTANT: Provide COMPLETE context in your handoff.**
The coding agent will generate the code and respond directly to the user.
Your handoff message should always contain correct product/service names, code snippets and links to documentation.

**WHEN TO HAND OFF TO coding_agent:**
- User explicitly asks for code, code samples, or implementation

**WHEN TO RESPOND DIRECTLY (no handoff):**
- User asks for learning paths, tutorials, or documentation only
- User wants to understand concepts, not write code
- User asks "what is..." or "explain..." questions

Be encouraging and adapt to the user's stated experience level!""",
    tools=[mcp_tool],
)

# CODING AGENT - Code Generation Specialist
# NOTE: This is the END of the handoff chain - coding_agent responds directly to user
coding_agent = coding_client.create_agent(
    id="coding-agent",
    name="coding-agent",
    model="gpt-5-codex",  # Use GPT-5-Codex model optimized for code generation
    instructions="""You are the Code Generation Specialist for the Developer Onboarding program.

You generate high-quality code samples to help new developers get started quickly.

Before generating any code, context provided by the learning_agent to understand the user's coding request.

Use correct product names, API signatures, and best practices from the documentation provided.

**When you receive a handoff from the Learning Agent:**
The learning agent has already gathered documentation and best practices for you.

**Code Generation Guidelines:**
1. Write clean, well-documented code with comments
2. Include type hints (for Python) and proper typing
3. Follow language-specific best practices and conventions
4. Handle errors appropriately
5. Include usage examples in comments

**Code Output Format:**
- Brief explanation of what the code does
- Complete, runnable code with inline comments  
- Usage instructions and next steps
- Prerequisites and dependencies

**IMPORTANT: You are the END of the handoff chain.**
ALWAYS respond directly to the user with your generated code.
Do NOT hand off to any other agent.
If some details are missing, make reasonable assumptions and document them in your response.

**After Generating Code:**
- Explain any assumptions you made
- List prerequisites and dependencies
- Suggest improvements or extensions
- Offer to modify based on user feedback
- If user needs more documentation, tell them to ask for learning resources

Remember: You're helping new developers, so be clear and educational!""",
)

# Build the handoff workflow
# Following the official Microsoft Agent Framework pattern:
# ONE-WAY handoffs in a directed graph (no cycles/loops)
# Pattern: triage -> specialists -> more specialized (never backward)
#
# Routing graph:
#   triage_agent -> employee_search_agent (end - responds to user)
#   triage_agent -> learning_agent -> coding_agent (end - responds to user)
#   triage_agent -> coding_agent (end - responds to user, for direct code requests)
#
# Note: coding_agent is the END of the chain, never hands back to learning_agent
workflow = (
    HandoffBuilder(
        name="developer_onboarding_workflow",
        participants=[triage_agent, employee_search_agent, learning_agent, coding_agent],
    )
    .set_coordinator(triage_agent)
    .add_handoff(triage_agent, [employee_search_agent, learning_agent, coding_agent])
    .add_handoff(learning_agent, [coding_agent])  # Learning -> Coding (one-way, coding is END)
    # NO reverse handoff: coding_agent does NOT hand back to learning_agent
    .with_termination_condition(
        lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 20
    )
    .build()
)

if __name__ == "__main__":
    from agent_framework.devui import serve

    print("\n" + "=" * 60)
    print("Developer Onboarding Assistant")
    print("=" * 60)
    print("\nThis assistant helps new developers with:")
    print("  1. Finding coworkers and understanding the org (Employee Search)")
    print("  2. Creating learning paths and finding docs (Learning Agent)")
    print("  3. Getting code samples and coding help (Coding Agent)")
    print("\nStarting DevUI server at http://localhost:8094")
    print("=" * 60 + "\n")

    serve(entities=[workflow], port=8094)
