# Use official Python image
FROM python:3.11-slim

ENV PULUMI_HOME="/root/.pulumi"

# Ensure 'curl' is installed, as it is required for the installation script
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh
ENV PATH="${PULUMI_HOME}/bin:$PATH"

ARG PULUMI_PLUGIN_LIST="aws@v7.16.0 datadog@v4.64.0"
RUN for plugin in $(echo $PULUMI_PLUGIN_LIST); do \
    provider=$(echo $plugin | cut -d'@' -f1); \
    version=$(echo $plugin | cut -d'@' -f2); \
    pulumi plugin install resource "$provider" "$version"; \
    done

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install uv && uv sync

# Run the app
CMD ["uv", "run", "main.py"]