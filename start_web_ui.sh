#!/bin/bash

# iDotMatrix Web UI Launcher
# This script starts the web-based user interface for controlling iDotMatrix displays

echo "🚀 Starting iDotMatrix Web Controller..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "my-venv" ]; then
    echo "📦 Activating virtual environment..."
    source my-venv/bin/activate
fi

# Check if required dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import http.server, json, subprocess" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing required Python modules"
    echo "Please ensure Python 3 is installed with standard libraries"
    exit 1
fi

# Start the web server
echo "🌐 Starting web server..."
python3 web_server.py --no-browser "$@"