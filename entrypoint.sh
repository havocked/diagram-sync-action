#!/bin/bash
set -e

export CONFLUENCE_URL="${INPUT_CONFLUENCE_URL}"
export CONFLUENCE_TOKEN="${INPUT_CONFLUENCE_TOKEN}"
export CONFLUENCE_USER="${INPUT_CONFLUENCE_USER}"
export CONFLUENCE_PAGE_ID="${INPUT_CONFLUENCE_PAGE_ID}"
export DIAGRAMS_DIR="${INPUT_DIAGRAMS_DIR:-docs/diagrams}"

cd /action
python -m src.diagram_sync.sync 