"""
One-time setup script to upload the employees file and create a vector store.
Run this once, then copy the VECTOR_STORE_ID to your .env file.

Usage:
    python setup_vector_store.py
"""

import asyncio
import os
from pathlib import Path

from azure.ai.agents.aio import AgentsClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()


async def setup():
    """Upload file and create vector store, print the ID for .env"""
    
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    
    async with AzureCliCredential() as creds:
        async with AgentsClient(endpoint=endpoint, credential=creds) as client:
            
            # Upload the employees file
            file_path = Path(__file__).parent / "data" / "employees.md"
            print(f"Uploading {file_path}...")
            
            file = await client.files.upload_and_poll(
                file_path=file_path,
                purpose="assistants"
            )
            print(f"  File ID: {file.id}")
            
            # Create vector store with the file
            print("Creating vector store...")
            vector_store = await client.vector_stores.create_and_poll(
                file_ids=[file.id],
                name="Employee Directory"
            )
            print(f"  Vector Store ID: {vector_store.id}")
            
            print("\n" + "=" * 60)
            print("Setup complete! Add this to your .env file:")
            print("=" * 60)
            print(f"\nVECTOR_STORE_ID={vector_store.id}\n")


if __name__ == "__main__":
    asyncio.run(setup())
