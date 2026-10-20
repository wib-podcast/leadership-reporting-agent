#!/bin/sh
# Runs the free n8n Community Edition on http://127.0.0.1:5678.
# Data and the credential encryption key live in ./.n8n (gitignored). Stop with Ctrl+C.
set -eu
REPO_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
export N8N_USER_FOLDER="$REPO_DIR"
export N8N_HOST=127.0.0.1
export N8N_LISTEN_ADDRESS=127.0.0.1
export N8N_PORT=5678
export N8N_SECURE_COOKIE=false
exec npx --yes n8n@2.43.8 start
