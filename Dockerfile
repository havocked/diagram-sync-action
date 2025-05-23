FROM python:3.11-slim

# Install Java
RUN apt-get update && apt-get install -y openjdk-17-jre wget && rm -rf /var/lib/apt/lists/*

# Install Rye
RUN pip install rye

# Download PlantUML
RUN wget https://github.com/plantuml/plantuml/releases/download/v1.2024.6/plantuml-1.2024.6.jar -O /plantuml.jar

# Set workdir
WORKDIR /action

# Copy code
COPY src/ /action/src/
COPY pyproject.toml /action/
COPY diagram-sync-action/entrypoint.sh /entrypoint.sh

# Install dependencies
RUN rye sync

ENTRYPOINT ["/entrypoint.sh"] 