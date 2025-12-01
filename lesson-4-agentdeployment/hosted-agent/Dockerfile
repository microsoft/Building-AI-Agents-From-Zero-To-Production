# Dockerfile for Developer Onboarding Multi-Agent Hosted Agent
# 
# This container runs the multi-agent workflow as a hosted agent
# on Azure AI Foundry. The agent server listens on port 8088.

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose the hosted agent port
EXPOSE 8088

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8088/health')" || exit 1

# Run the hosted agent
CMD ["python", "main.py"]
