"""
Agent Evaluations - Developer Onboarding Assistant with Azure AI Evaluation

This application demonstrates multi-agent workflow evaluation using Azure AI services.
It helps new developers onboard to a company by orchestrating multiple specialized 
agents using the Microsoft Agent Framework's HandoffBuilder pattern, and then evaluates 
the agent responses using Azure AI cloud-based evaluators.

Routing Scenarios:
1. Organizational Questions → Employee Search Agent (search employee data)
2. Training Materials → Learning Agent (create learning paths)
3. Coding Help → Learning Agent (pulls docs) → Coding Agent (generates code)

Evaluation Workflow:
1. Execute the multi-agent handoff workflow
2. Track response IDs and conversation IDs for each agent
3. Create evaluations using Azure AI evaluators (relevance, groundedness, etc.)
4. Run evaluations and monitor progress
5. Display evaluation results and report URL

Prerequisites:
1. Ensure you have Azure CLI credentials configured (run `az login`)
2. Azure AI Project endpoint configured in environment variables:
   - AZURE_AI_PROJECT_ENDPOINT

Usage:
    python agent-evals.py
"""

import asyncio
import os
import time
from collections import defaultdict

from azure.ai.projects import AIProjectClient
from azure.ai.projects.aio import AIProjectClient as AsyncAIProjectClient
from azure.identity import DefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential as AsyncDefaultAzureCredential
from dotenv import load_dotenv

from agent_framework import (
    AgentRunUpdateEvent,
    AgentRunResponseUpdate,
    ChatMessage,
    HandoffBuilder,
    HandoffUserInputRequest,
    HostedFileSearchTool,
    HostedMCPTool,
    HostedVectorStoreContent,
    RequestInfoEvent,
    Role,
    WorkflowOutputEvent,
    WorkflowStatusEvent,
    WorkflowRunState,
)
from agent_framework.azure import AzureAIClient

load_dotenv()


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")


async def create_agents(project_client, credential):
    """Create all specialized agents for the onboarding workflow.
    
    Each agent gets its own AzureAIClient instance with store=True to ensure
    responses are persisted in Azure AI for evaluation.
    """
    
    # Create separate client for each agent (required for proper response tracking)
    triage_client = AzureAIClient(
        project_client=project_client,
        async_credential=credential,
        agent_name="triage-agent"
    )
    
    employee_client = AzureAIClient(
        project_client=project_client,
        async_credential=credential,
        agent_name="employee-search-agent"
    )
    
    learning_client = AzureAIClient(
        project_client=project_client,
        async_credential=credential,
        agent_name="learning-agent"
    )
    
    coding_client = AzureAIClient(
        project_client=project_client,
        async_credential=credential,
        agent_name="coding-agent"
    )

    # TRIAGE AGENT - The Coordinator
    triage_agent = triage_client.create_agent(
        id="triage-agent",
        name="triage-agent",
        store=True,
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

    # Create the file search tool with pre-created vector store
    file_search_tool = HostedFileSearchTool(
        inputs=[
            HostedVectorStoreContent(
                vector_store_id=os.environ["VECTOR_STORE_ID"]
            )
        ]
    )

    # EMPLOYEE SEARCH AGENT - Organizational Knowledge Specialist
    employee_search_agent = employee_client.create_agent(
        id="employee-search-agent",
        name="employee-search-agent",
        store=True,
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
        store=True,
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
        tools=[mcp_tool],
    )

    # CODING AGENT - Code Generation Specialist
    coding_agent = coding_client.create_agent(
        id="coding-agent",
        name="coding-agent",
        model="gpt-5-codex",  # Use GPT-5-Codex model optimized for code generation
        store=True,
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

    clients = [triage_client, employee_client, learning_client, coding_client]
    return triage_agent, employee_search_agent, learning_agent, coding_agent, clients


def build_handoff_workflow(triage, employee_search, learning, coding):
    """Build the handoff workflow with routing rules."""
    workflow = (
        HandoffBuilder(
            name="developer_onboarding_workflow",
            participants=[triage, employee_search, learning, coding],
        )
        .set_coordinator(triage)
        .add_handoff(triage, [employee_search, learning, coding])
        .add_handoff(learning, [coding])
        .with_termination_condition(
            lambda conv: sum(1 for msg in conv if msg.role.value == "user") >= 20
        )
        .build()
    )
    return workflow


def _track_agent_ids(event, agent: str, response_ids: dict, conversation_ids: dict):
    """Track agent response and conversation IDs from AgentRunUpdateEvent."""
    if isinstance(event.data, AgentRunResponseUpdate):
        if hasattr(event.data, 'raw_representation') and event.data.raw_representation:
            raw = event.data.raw_representation
            
            if hasattr(raw, 'conversation_id') and raw.conversation_id:
                if raw.conversation_id not in conversation_ids[agent]:
                    conversation_ids[agent].append(raw.conversation_id)
            
            if hasattr(raw, 'raw_representation') and raw.raw_representation:
                openai_event = raw.raw_representation
                if hasattr(openai_event, 'response') and hasattr(openai_event.response, 'id'):
                    if openai_event.response.id not in response_ids[agent]:
                        response_ids[agent].append(openai_event.response.id)


async def run_workflow_with_response_tracking(query: str) -> dict:
    """Execute the multi-agent onboarding workflow and track response IDs."""
    print_section("Step 1: Running Developer Onboarding Workflow")
    print(f"Query: {query}")
    print("Executing multi-agent handoff workflow...\n")
    
    conversation_ids = defaultdict(list)
    response_ids = defaultdict(list)
    workflow_output = None
    conversation_messages = []
    
    async with AsyncDefaultAzureCredential() as credential:
        project_client = AsyncAIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=credential,
            api_version="2025-11-15-preview",
        )
        
        async with project_client:
            triage, employee_search, learning, coding, clients = await create_agents(
                project_client, credential
            )
            workflow = build_handoff_workflow(triage, employee_search, learning, coding)
            
            initial_message = ChatMessage(role=Role.USER, text=query)
            events = workflow.run_stream([initial_message])
            
            async for event in events:
                print(f"[Event Type]: {type(event).__name__}")
                
                if isinstance(event, WorkflowOutputEvent):
                    workflow_output = event.data
                    if isinstance(event.data, list):
                        conversation_messages = event.data
                        for msg in reversed(event.data):
                            if hasattr(msg, 'role') and msg.role == Role.ASSISTANT and msg.text:
                                print(f"\n[Workflow Output]: {msg.text[:500]}...")
                                break
                    else:
                        print(f"\n[Workflow Output]: {event.data}")
                
                elif isinstance(event, RequestInfoEvent):
                    if isinstance(event.data, HandoffUserInputRequest):
                        conversation_messages = event.data.conversation
                        print(f"\n[Agent Conversation Captured]: {len(conversation_messages)} messages")
                        
                        for msg in conversation_messages:
                            if hasattr(msg, 'author_name') and msg.author_name and hasattr(msg, 'text') and msg.text:
                                agent_name = msg.author_name
                                if agent_name not in ["user", None]:
                                    print(f"  - {agent_name}: {msg.text[:100]}...")
                    
                elif isinstance(event, AgentRunUpdateEvent):
                    agent_name = event.executor_id if hasattr(event, 'executor_id') else "unknown"
                    print(f"[Agent Update]: {agent_name}")
                    
                    if hasattr(event, 'data'):
                        _track_agent_ids(event, agent_name, response_ids, conversation_ids)
                        
                elif isinstance(event, WorkflowStatusEvent):
                    print(f"[Status]: {event.state.name}")
    
    output_data = {
        "agents": {},
        "query": query,
        "output": workflow_output,
        "conversation": conversation_messages
    }
    
    all_agents = set(conversation_ids.keys()) | set(response_ids.keys())
    
    for agent_name in all_agents:
        output_data["agents"][agent_name] = {
            "conversation_ids": conversation_ids.get(agent_name, []),
            "response_ids": response_ids.get(agent_name, []),
            "response_count": len(response_ids.get(agent_name, []))
        }
    
    print(f"\nWorkflow execution completed")
    print(f"Total agents tracked: {len(output_data['agents'])}")
    
    print("\n=== Response Summary ===")
    for agent_name, agent_data in output_data["agents"].items():
        response_count = agent_data["response_count"]
        print(f"{agent_name}: {response_count} response(s)")
    
    return output_data


def display_response_summary(workflow_data: dict):
    """Display summary of response data from the workflow."""
    print_section("Step 2: Response Data Summary")
    
    print(f"Query: {workflow_data['query']}")
    print(f"\nAgents tracked: {len(workflow_data['agents'])}")
    
    for agent_name, agent_data in workflow_data['agents'].items():
        response_count = agent_data['response_count']
        print(f"  {agent_name}: {response_count} response(s)")
        if agent_data['response_ids']:
            for i, resp_id in enumerate(agent_data['response_ids'][:3], 1):
                print(f"    Response {i}: {resp_id}")


def fetch_agent_responses(openai_client, workflow_data: dict, agent_names: list):
    """Fetch and display final responses from specified agents."""
    print_section("Step 3: Fetching Agent Responses")
    
    for agent_name in agent_names:
        if agent_name not in workflow_data['agents']:
            continue
            
        agent_data = workflow_data['agents'][agent_name]
        if not agent_data['response_ids']:
            continue
        
        final_response_id = agent_data['response_ids'][-1]
        print(f"\n{agent_name}")
        print(f"  Response ID: {final_response_id}")
        
        try:
            response = openai_client.responses.retrieve(response_id=final_response_id)
            content = response.output[-1].content[-1].text
            truncated = content[:300] + "..." if len(content) > 300 else content
            print(f"  Content preview: {truncated}")
        except Exception as e:
            print(f"  Error: {e}")


def create_evaluation(openai_client, model_deployment: str):
    """Create evaluation with Azure AI evaluators."""
    print_section("Step 4: Creating Evaluation")
    
    data_source_config = {"type": "azure_ai_source", "scenario": "responses"}
    
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "relevance",
            "evaluator_name": "builtin.relevance",
            "initialization_parameters": {"deployment_name": model_deployment}
        },
        {
            "type": "azure_ai_evaluator",
            "name": "groundedness",
            "evaluator_name": "builtin.groundedness",
            "initialization_parameters": {"deployment_name": model_deployment}
        },
        {
            "type": "azure_ai_evaluator",
            "name": "tool_call_accuracy",
            "evaluator_name": "builtin.tool_call_accuracy",
            "initialization_parameters": {"deployment_name": model_deployment}
        },
        {
            "type": "azure_ai_evaluator",
            "name": "tool_output_utilization",
            "evaluator_name": "builtin.tool_output_utilization",
            "initialization_parameters": {"deployment_name": model_deployment}
        },
    ]
    
    eval_object = openai_client.evals.create(
        name="Developer Onboarding Workflow Evaluation",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    
    evaluator_names = [criterion["name"] for criterion in testing_criteria]
    print(f"Evaluation created: {eval_object.id}")
    print(f"Evaluators ({len(evaluator_names)}): {', '.join(evaluator_names)}")
    
    return eval_object


def run_evaluation(openai_client, eval_object, workflow_data: dict, agent_names: list):
    """Run evaluation on selected agent responses."""
    print_section("Step 5: Running Evaluation")
    
    selected_response_ids = []
    for agent_name in agent_names:
        if agent_name in workflow_data['agents']:
            agent_data = workflow_data['agents'][agent_name]
            if agent_data['response_ids']:
                selected_response_ids.append(agent_data['response_ids'][-1])
    
    print(f"Selected {len(selected_response_ids)} responses for evaluation")
    
    data_source = {
        "type": "azure_ai_responses",
        "item_generation_params": {
            "type": "response_retrieval",
            "data_mapping": {"response_id": "{{item.resp_id}}"},
            "source": {
                "type": "file_content",
                "content": [{"item": {"resp_id": resp_id}} for resp_id in selected_response_ids]
            },
        },
    }
    
    eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id,
        name="Developer Onboarding Evaluation Run",
        data_source=data_source
    )
    
    print(f"Evaluation run created: {eval_run.id}")
    
    return eval_run


def monitor_evaluation(openai_client, eval_object, eval_run):
    """Monitor evaluation progress and display results."""
    print_section("Step 6: Monitoring Evaluation")
    
    print("Waiting for evaluation to complete...")
    
    while eval_run.status not in ["completed", "failed"]:
        eval_run = openai_client.evals.runs.retrieve(
            run_id=eval_run.id,
            eval_id=eval_object.id
        )
        print(f"Status: {eval_run.status}")
        time.sleep(5)
    
    if eval_run.status == "completed":
        print("\nEvaluation completed successfully")
        print(f"Result counts: {eval_run.result_counts}")
        print(f"\nReport URL: {eval_run.report_url}")
    else:
        print("\nEvaluation failed")


async def run_evaluation_workflow():
    """Main evaluation workflow - runs agents and evaluates responses."""
    
    example_queries = [
        "I'm new here! Has anyone worked at Microsoft here?",
        "Can you help me find colleagues who came from Google and create a learning path for Python development?",
        "Who manages the platform team? Also, I need to learn about Azure Functions - can you create a training plan?",
    ]
    
    query = example_queries[0]
    
    workflow_data = await run_workflow_with_response_tracking(query)
    
    display_response_summary(workflow_data)
    
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
        api_version="2025-11-15-preview"
    )
    openai_client = project_client.get_openai_client()
    
    agents_to_evaluate = ["triage-agent", "employee-search-agent", "learning-agent", "coding-agent"]
    
    fetch_agent_responses(openai_client, workflow_data, agents_to_evaluate)
    
    model_deployment = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o")
    eval_object = create_evaluation(openai_client, model_deployment)
    
    eval_run = run_evaluation(openai_client, eval_object, workflow_data, agents_to_evaluate)
    
    monitor_evaluation(openai_client, eval_object, eval_run)
    
    print_section("Evaluation Complete")
    
    return workflow_data


if __name__ == "__main__":
    asyncio.run(run_evaluation_workflow())
