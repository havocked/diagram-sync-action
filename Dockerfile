FROM python:3.11-slim

# Install Java and wget
RUN apt-get update && apt-get install -y openjdk-17-jre wget && rm -rf /var/lib/apt/lists/*

# Download PlantUML
RUN wget https://github.com/plantuml/plantuml/releases/download/v1.2024.6/plantuml-1.2024.6.jar -O /plantuml.jar

WORKDIR /action

# Copy code and dependencies
COPY src/ /action/src/
COPY pyproject.toml /action/
COPY requirements.txt /action/
COPY entrypoint.sh /entrypoint.sh

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r /action/requirements.txt

ENTRYPOINT ["/entrypoint.sh"] 