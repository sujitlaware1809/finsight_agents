#!/bin/bash

echo "Starting FinSight AI Local Server..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    echo "Please install pip and try again"
    exit 1
fi

# Check if requirements are installed
if ! pip3 show fastapi &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements_local.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo
echo "🚀 Starting FinSight AI Local Development Server..."
echo "📍 Server URL: http://localhost:8000"
echo "📋 Demo Page: frontend_demo.html"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python3 local_server.py

echo
echo "Server stopped."
