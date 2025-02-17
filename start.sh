#!/bin/bash

# Start Python Flask server in the background
cd server/python && python3 app.py &

# Wait a moment for Flask to start
sleep 2

# Start Node.js server
npm run dev
