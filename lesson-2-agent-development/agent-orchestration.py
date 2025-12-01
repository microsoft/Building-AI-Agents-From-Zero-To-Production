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
learning_agent = learning_client.create_agent(
    id="learning-agent",
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
)

# CODING AGENT - Code Generation Specialist
coding_agent = coding_client.create_agent(
    id="coding-agent",
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

# Build the handoff workflow
workflow = (
    HandoffBuilder(
        name="developer_onboarding_workflow",
        participants=[triage_agent, employee_search_agent, learning_agent, coding_agent],
    )
    .set_coordinator(triage_agent)
    .add_handoff(triage_agent, [employee_search_agent, learning_agent, coding_agent])
    .add_handoff(learning_agent, [coding_agent])
    .add_handoff(coding_agent, [learning_agent])
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
