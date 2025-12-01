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
2. Azure OpenAI deployment: gpt-4o

    python agent-orchestration.py
    
Then open http://localhost:8094 in your browser.
"""

import asyncio
import logging
from collections.abc import AsyncIterable
from typing import cast

from azure.identity import AzureCliCredential
from dotenv import load_dotenv

from agent_framework import (
    ChatMessage,
    HandoffBuilder,
    HandoffUserInputRequest,
    RequestInfoEvent,
    WorkflowEvent,
    WorkflowOutputEvent,
    WorkflowRunState,
    WorkflowStatusEvent,
)
from agent_framework.azure import AzureOpenAIChatClient

# Enable logging to see orchestration activity
logging.basicConfig(level=logging.INFO)
logging.getLogger("agent_framework").setLevel(logging.DEBUG)

# Load environment variables
load_dotenv()


def create_agents(chat_client: AzureOpenAIChatClient):
    """Create all specialized agents for the onboarding workflow.
    
    Args:
        chat_client: Client for all agents (gpt-4o deployment)
    
    Returns:
        Tuple of (triage_agent, employee_search_agent, learning_agent, coding_agent)
    """
    
    # ==========================================================================
    # TRIAGE AGENT - The Coordinator
    # ==========================================================================
    triage_agent = chat_client.create_agent(
        name="triage_agent",
        instructions="""You are the Developer Onboarding Assistant - a friendly coordinator helping new developers get settled at their new company.

Your role is to understand what the new developer needs and route them to the right specialist:

1. **Organizational Questions** → Hand off to employee_search_agent
   - Questions about coworkers, teams, managers
   - Finding people from the same former company
   - Understanding the org structure
   - Examples: "Who is on my team?", "Is anyone else from my former company here?", "Who manages the AI team?"

2. **Training & Learning** → Hand off to learning_agent
   - Creating learning paths and training plans
   - Finding documentation and tutorials
   - Understanding technologies used at the company
   - Examples: "I need to learn Azure", "Create a training plan for Python", "What should I learn first?"

3. **Coding Help & Code Samples** → Hand off to learning_agent FIRST
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
    
    # ==========================================================================
    # EMPLOYEE SEARCH AGENT - Organizational Knowledge Specialist
    # ==========================================================================
    employee_search_agent = chat_client.create_agent(
        name="employee_search_agent",
        instructions="""You are the Employee Search Specialist for the Developer Onboarding program at Zava, a software company.

You help new developers learn about their coworkers and the organization structure.

You have knowledge about the following employees at Zava:
- Sarah Chen: AI Engineering Team Lead, former Google engineer, joined 2022
- Marcus Johnson: Senior Platform Engineer, former Amazon, joined 2021
- Priya Patel: ML Engineer on AI Team, former Meta, joined 2023
- David Kim: Backend Developer on Platform Team, former Microsoft, joined 2022
- Emma Wilson: DevOps Engineer, former Netflix, joined 2023
- James Rodriguez: Frontend Developer, former Airbnb, joined 2022
- Lisa Thompson: Product Manager for AI Products, former LinkedIn, joined 2021
- Alex Kumar: Data Scientist on AI Team, former Uber, joined 2023
- Rachel Green: QA Engineer, former Spotify, joined 2022
- Michael Brown: Security Engineer, former Apple, joined 2021

When asked questions about employees:
- Search through this employee data to find relevant matches
- Provide helpful details like team, role, former company, and join date
- Be warm and welcoming - help them feel connected to their new colleagues

After answering organizational questions, ask if they need help with anything else:
- Learning resources for technologies used at the company
- Code samples for common tasks
- More information about specific people or teams""",
    )
    
    # ==========================================================================
    # LEARNING AGENT - Training & Documentation Specialist
    # ==========================================================================
    learning_agent = chat_client.create_agent(
        name="learning_agent",
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
    
    # ==========================================================================
    # CODING AGENT - Code Generation Specialist
    # ==========================================================================
    # Uses gpt-4o which is also excellent at code generation
    coding_agent = chat_client.create_agent(
        name="coding_agent",
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
    
    return triage_agent, employee_search_agent, learning_agent, coding_agent


def build_handoff_workflow(triage, employee_search, learning, coding):
    """Build the handoff workflow with routing rules.
    
    Routing Pattern:
    - User → Triage → Employee Search (for org questions)
    - User → Triage → Learning → (optionally) Coding (for training/coding)
    - Learning Agent can hand off to Coding Agent for code generation
    - Coding Agent can hand off back to Learning Agent if more context needed
    """
    workflow = (
        HandoffBuilder(
            name="developer_onboarding_workflow",
            participants=[triage, employee_search, learning, coding],
        )
        .set_coordinator(triage)  # Pass agent object, not string
        # Triage can route to all specialists
        .add_handoff(triage, [employee_search, learning, coding])
        # Learning agent can hand off to coding agent for code generation
        .add_handoff(learning, [coding])
        # Coding agent can hand off back to learning agent if needed
        .add_handoff(coding, [learning])
        # Allow conversation to continue until user is satisfied
        .with_termination_condition(
            # Terminate after 20 user messages (allow for extended onboarding sessions)
            lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 20
        )
        .build()
    )
    
    return workflow


async def _drain(stream: AsyncIterable[WorkflowEvent]) -> list[WorkflowEvent]:
    """Collect all events from an async stream into a list."""
    return [event async for event in stream]


def _handle_events(events: list[WorkflowEvent]) -> list[RequestInfoEvent]:
    """Process workflow events and extract pending user input requests."""
    requests: list[RequestInfoEvent] = []

    for event in events:
        if isinstance(event, WorkflowStatusEvent) and event.state in {
            WorkflowRunState.IDLE,
            WorkflowRunState.IDLE_WITH_PENDING_REQUESTS,
        }:
            print(f"[status] {event.state.name}")

        elif isinstance(event, WorkflowOutputEvent):
            conversation = cast(list[ChatMessage], event.data)
            if isinstance(conversation, list):
                print("\n=== Conversation Update ===")
                for message in conversation:
                    if not message.text.strip():
                        continue
                    speaker = message.author_name or message.role.value
                    print(f"- {speaker}: {message.text}")
                print("===========================")

        elif isinstance(event, RequestInfoEvent):
            if isinstance(event.data, HandoffUserInputRequest):
                _print_handoff_request(event.data)
            requests.append(event)

    return requests


def _print_handoff_request(request: HandoffUserInputRequest) -> None:
    """Display a user input request with conversation context."""
    print("\n=== Agent Response ===")
    messages_with_text = [msg for msg in request.conversation if msg.text.strip()]
    for message in messages_with_text[-3:]:
        speaker = message.author_name or message.role.value
        text = message.text[:200] + "..." if len(message.text) > 200 else message.text
        print(f"  {speaker}: {text}")
    print("======================")


def run_with_devui():
    """Run the workflow with DevUI for interactive chat."""
    from agent_framework.devui import serve
    
    credential = AzureCliCredential()
    
    # Azure OpenAI endpoint
    endpoint = "https://aiteam-aiservice2601.openai.azure.com/"
    
    # Initialize chat client with gpt-4o for all agents
    chat_client = AzureOpenAIChatClient(
        credential=credential,
        endpoint=endpoint,
        deployment_name="gpt-4o",
    )
    
    # Create all agents
    print("Creating specialized agents...")
    triage, employee_search, learning, coding = create_agents(chat_client)
    
    # Build the handoff workflow
    print("Building handoff workflow...")
    workflow = build_handoff_workflow(triage, employee_search, learning, coding)
    
    print("\n" + "=" * 60)
    print("Developer Onboarding Assistant")
    print("=" * 60)
    print("\nThis assistant helps new developers with:")
    print("  1. Finding coworkers and understanding the org (Employee Search)")
    print("  2. Creating learning paths and finding docs (Learning Agent)")
    print("  3. Getting code samples and coding help (Coding Agent)")
    print("\nStarting DevUI server at http://localhost:8094")
    print("=" * 60 + "\n")
    
    # Serve the workflow with DevUI
    serve(entities=[workflow], port=8094)


if __name__ == "__main__":
    run_with_devui()
