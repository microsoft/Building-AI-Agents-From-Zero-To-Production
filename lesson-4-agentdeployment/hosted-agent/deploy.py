"""
Deploy Hosted Agent to Azure AI Foundry

This script deploys the multi-agent workflow as a hosted agent using the
Azure AI Projects SDK. It handles:
1. Building and pushing the Docker image to ACR
2. Creating the hosted agent version in Azure AI Foundry
3. Starting the agent deployment

Prerequisites:
- Azure CLI authenticated (`az login`)
- Docker installed and running
- Azure Container Registry created
- Container Registry Repository Reader role assigned to project's managed identity

Usage:
    python deploy.py --build      # Build and push Docker image, then deploy
    python deploy.py --deploy     # Deploy only (image already in ACR)
    python deploy.py --start      # Start an existing agent deployment
    python deploy.py --stop       # Stop an agent deployment
    python deploy.py --status     # Check agent status
"""

import argparse
import os
import subprocess
import sys
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)
from azure.identity import DefaultAzureCredential

# Configuration - Update these values or use environment variables
PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
ACR_NAME = os.environ.get("ACR_NAME", "your-acr-name")
IMAGE_NAME = os.environ.get("IMAGE_NAME", "developer-onboarding-agent")
IMAGE_TAG = os.environ.get("IMAGE_TAG", "latest")
AGENT_NAME = os.environ.get("AGENT_NAME", "developer-onboarding-workflow")
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")
MODEL_DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-4o")

# Resource allocation
CPU = os.environ.get("AGENT_CPU", "1")
MEMORY = os.environ.get("AGENT_MEMORY", "2Gi")
MIN_REPLICAS = int(os.environ.get("AGENT_MIN_REPLICAS", "1"))
MAX_REPLICAS = int(os.environ.get("AGENT_MAX_REPLICAS", "2"))


def get_full_image_url():
    """Get the full ACR image URL."""
    return f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}"


def build_and_push_image():
    """Build the Docker image and push to Azure Container Registry."""
    print("=" * 60)
    print("Building and pushing Docker image to ACR")
    print("=" * 60)
    
    image_url = get_full_image_url()
    
    # Build the Docker image
    print(f"\n📦 Building Docker image: {IMAGE_NAME}:{IMAGE_TAG}")
    result = subprocess.run(
        ["docker", "build", "-t", f"{IMAGE_NAME}:{IMAGE_TAG}", "."],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Docker build failed:\n{result.stderr}")
        sys.exit(1)
    print("✅ Docker image built successfully")
    
    # Login to ACR
    print(f"\n🔐 Logging in to Azure Container Registry: {ACR_NAME}")
    result = subprocess.run(
        ["az", "acr", "login", "--name", ACR_NAME],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ ACR login failed:\n{result.stderr}")
        sys.exit(1)
    print("✅ Logged in to ACR")
    
    # Tag the image for ACR
    print(f"\n🏷️  Tagging image for ACR: {image_url}")
    result = subprocess.run(
        ["docker", "tag", f"{IMAGE_NAME}:{IMAGE_TAG}", image_url],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Docker tag failed:\n{result.stderr}")
        sys.exit(1)
    print("✅ Image tagged")
    
    # Push to ACR
    print(f"\n📤 Pushing image to ACR: {image_url}")
    result = subprocess.run(
        ["docker", "push", image_url],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Docker push failed:\n{result.stderr}")
        sys.exit(1)
    print("✅ Image pushed to ACR")
    
    return image_url


def create_agent_version(image_url: str):
    """Create a new hosted agent version in Azure AI Foundry."""
    print("\n" + "=" * 60)
    print("Creating hosted agent version in Azure AI Foundry")
    print("=" * 60)
    
    print(f"\n📋 Configuration:")
    print(f"   Project Endpoint: {PROJECT_ENDPOINT}")
    print(f"   Agent Name: {AGENT_NAME}")
    print(f"   Container Image: {image_url}")
    print(f"   CPU: {CPU}, Memory: {MEMORY}")
    print(f"   Replicas: {MIN_REPLICAS}-{MAX_REPLICAS}")
    
    # Initialize client
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )
    
    # Create agent version
    print(f"\n🚀 Creating agent version...")
    agent = client.agents.create_version(
        agent_name=AGENT_NAME,
        definition=ImageBasedHostedAgentDefinition(
            container_protocol_versions=[
                ProtocolVersionRecord(
                    protocol=AgentProtocol.RESPONSES,
                    version="v1"
                )
            ],
            cpu=CPU,
            memory=MEMORY,
            image=image_url,
            environment_variables={
                "AZURE_AI_PROJECT_ENDPOINT": PROJECT_ENDPOINT,
                "VECTOR_STORE_ID": VECTOR_STORE_ID or "",
                "MODEL_DEPLOYMENT": MODEL_DEPLOYMENT,
            }
        )
    )
    
    print(f"✅ Agent version created successfully!")
    print(f"   Agent ID: {agent.id}")
    print(f"   Agent Name: {agent.name}")
    
    return agent


def start_agent():
    """Start the hosted agent deployment using Azure CLI."""
    print("\n" + "=" * 60)
    print("Starting hosted agent deployment")
    print("=" * 60)
    
    # Parse account and project from endpoint
    # Endpoint format: https://<account>.services.ai.azure.com/api/projects/<project>
    parts = PROJECT_ENDPOINT.replace("https://", "").split("/")
    account_name = parts[0].split(".")[0]
    project_name = parts[-1] if parts[-1] else parts[-2]
    
    print(f"\n📋 Starting agent:")
    print(f"   Account: {account_name}")
    print(f"   Project: {project_name}")
    print(f"   Agent: {AGENT_NAME}")
    
    result = subprocess.run([
        "az", "cognitiveservices", "agent", "start",
        "--account-name", account_name,
        "--project-name", project_name,
        "--name", AGENT_NAME,
        "--agent-version", "1"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to start agent:\n{result.stderr}")
        print("\n💡 You may need to start the agent from the Azure AI Foundry portal")
        return False
    
    print("✅ Agent deployment started!")
    return True


def stop_agent():
    """Stop the hosted agent deployment using Azure CLI."""
    print("\n" + "=" * 60)
    print("Stopping hosted agent deployment")
    print("=" * 60)
    
    parts = PROJECT_ENDPOINT.replace("https://", "").split("/")
    account_name = parts[0].split(".")[0]
    project_name = parts[-1] if parts[-1] else parts[-2]
    
    result = subprocess.run([
        "az", "cognitiveservices", "agent", "stop",
        "--account-name", account_name,
        "--project-name", project_name,
        "--name", AGENT_NAME,
        "--agent-version", "1"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Failed to stop agent:\n{result.stderr}")
        return False
    
    print("✅ Agent deployment stopped!")
    return True


def get_agent_status():
    """Get the status of the hosted agent."""
    print("\n" + "=" * 60)
    print("Checking hosted agent status")
    print("=" * 60)
    
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )
    
    try:
        agent = client.agents.retrieve(agent_name=AGENT_NAME)
        print(f"\n✅ Agent found:")
        print(f"   Name: {agent.name}")
        print(f"   ID: {agent.id}")
        if hasattr(agent, 'status'):
            print(f"   Status: {agent.status}")
        return agent
    except Exception as e:
        print(f"❌ Failed to retrieve agent: {e}")
        return None


def test_agent():
    """Test the deployed agent with a sample query."""
    print("\n" + "=" * 60)
    print("Testing hosted agent")
    print("=" * 60)
    
    from azure.ai.projects.models import AgentReference
    
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential()
    )
    
    # Get OpenAI client
    openai_client = client.get_openai_client()
    
    # Test query
    test_message = "Hello! I'm a new developer. What can you help me with?"
    print(f"\n📤 Sending test message: {test_message}")
    
    try:
        response = openai_client.responses.create(
            input=[{"role": "user", "content": test_message}],
            extra_body={
                "agent": AgentReference(
                    name=AGENT_NAME,
                    version="1"
                ).as_dict()
            }
        )
        
        print(f"\n📥 Agent response:")
        print("-" * 40)
        print(response.output_text)
        print("-" * 40)
        print("\n✅ Agent is responding correctly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Deploy and manage hosted agents on Azure AI Foundry"
    )
    parser.add_argument(
        "--build", action="store_true",
        help="Build Docker image, push to ACR, and deploy"
    )
    parser.add_argument(
        "--deploy", action="store_true",
        help="Deploy agent (assumes image already in ACR)"
    )
    parser.add_argument(
        "--start", action="store_true",
        help="Start the agent deployment"
    )
    parser.add_argument(
        "--stop", action="store_true",
        help="Stop the agent deployment"
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Check agent status"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Test the deployed agent"
    )
    
    args = parser.parse_args()
    
    # Validate configuration
    if not PROJECT_ENDPOINT:
        print("❌ Error: AZURE_AI_PROJECT_ENDPOINT environment variable not set")
        sys.exit(1)
    
    if args.build:
        image_url = build_and_push_image()
        create_agent_version(image_url)
        print("\n💡 Next step: Start the agent with --start or from Azure AI Foundry portal")
        
    elif args.deploy:
        image_url = get_full_image_url()
        create_agent_version(image_url)
        print("\n💡 Next step: Start the agent with --start or from Azure AI Foundry portal")
        
    elif args.start:
        start_agent()
        
    elif args.stop:
        stop_agent()
        
    elif args.status:
        get_agent_status()
        
    elif args.test:
        test_agent()
        
    else:
        parser.print_help()
        print("\n" + "=" * 60)
        print("Quick Start:")
        print("=" * 60)
        print("1. Set environment variables in .env file")
        print("2. Run: python deploy.py --build    # Build, push, and create agent")
        print("3. Run: python deploy.py --start    # Start the deployment")
        print("4. Run: python deploy.py --test     # Test the agent")


if __name__ == "__main__":
    main()
