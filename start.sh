#!/bin/bash

# Create log directory if it doesn't exist
mkdir -p logs

# Kill any existing processes on ports 8000 and 5000
pkill -f "python3 app.py" || true
pkill -f "npm run dev" || true

# Start Python Flask server in the background
cd server/python && python3 app.py > ../../logs/flask.log 2>&1 &

# Wait for Flask server to start
echo "Starting Flask server..."
sleep 3

# Check if Flask server is running
if curl -s http://localhost:8000/api/test > /dev/null; then
    echo "Flask server is running on port 8000"
else
    echo "Flask server failed to start. Check logs/flask.log for details"
    exit 1
fi

# Start Node.js server
echo "Starting Node.js server..."
npm run dev