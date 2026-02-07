# Use official Python image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

ENV PULUMI_HOME="/app/.pulumi"

RUN mkdir -p ${PULUMI_HOME}
# Ensure 'curl' is installed, as it is required for the installation script
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh -s -- --install-root ${PULUMI_HOME}
ENV PATH="${PULUMI_HOME}/bin:$PATH"
RUN export PATH="${PULUMI_HOME}/bin:$PATH"

# preload plugins. Airgapped environment might need this.
ARG PULUMI_PLUGIN_LIST="aws@v7.16.0 datadog@v4.64.0"
RUN for plugin in $(echo $PULUMI_PLUGIN_LIST); do \
    provider=$(echo $plugin | cut -d'@' -f1); \
    version=$(echo $plugin | cut -d'@' -f2); \
    pulumi plugin install resource "$provider" "$version"; \
    done

# Copy project files
COPY . /app
# Install Python dependencies
RUN pip install --upgrade pip && pip install uv && uv sync

EXPOSE 8000
# Run the app
CMD ["uv", "run", "main.py", "local-workspace", "run", "--help"]