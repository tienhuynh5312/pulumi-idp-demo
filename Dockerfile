# Use official Python image
FROM python:3.11-slim

ENV PULUMI_HOME="/root/.pulumi"

# Ensure 'curl' is installed, as it is required for the installation script
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install uv && uv sync

ENV PATH="${PULUMI_HOME}/bin:$PATH"
ENV PULUMI_AWS_PLUGIN_VERSION="v7.16.0"
RUN pulumi plugin install resource aws ${PULUMI_AWS_PLUGIN_VERSION}

# Run the app
CMD ["uv", "run", "main.py"]