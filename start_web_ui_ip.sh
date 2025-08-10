#!/bin/bash

# iDotMatrix Web UI Launcher for IP/Domain with HTTPS
# Usage: ./start_web_ui_ip.sh [ip_or_domain] [email_for_letsencrypt]

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/server_config.json"

# Read from config file if no arguments provided
if [ -z "$1" ] && [ -f "$CONFIG_FILE" ]; then
    echo "📄 Reading configuration from server_config.json..."
    DOMAIN=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['domain'])" 2>/dev/null)
    EMAIL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['email'])" 2>/dev/null)
else
    DOMAIN="$1"
    EMAIL="$2"
fi

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 [ip_or_domain] [email_for_letsencrypt]"
    echo "Example: $0 192.168.1.100"
    echo "Example: $0 mydomain.com user@example.com"
    echo "Or configure server_config.json with domain and email"
    exit 1
fi

echo "🔒 Starting iDotMatrix Web Controller with HTTPS for $DOMAIN..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "my-venv" ]; then
    echo "📦 Activating virtual environment..."
    source my-venv/bin/activate
fi

# Start the web server
echo "🌐 Starting HTTPS web server..."
if [ -n "$EMAIL" ]; then
    python3 web_server.py --no-browser --domain "$DOMAIN" --email "$EMAIL" --port 443
else
    python3 web_server.py --no-browser --domain "$DOMAIN" --port 443
fi