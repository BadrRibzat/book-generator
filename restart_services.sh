#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Book Generator - Restart Services ===${NC}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}tmux is not installed. Please install it first.${NC}"
    exit 1
fi

# Kill existing tmux session if it exists
tmux kill-session -t book-generator 2>/dev/null

# Create a new tmux session
echo -e "${GREEN}Creating tmux session...${NC}"
tmux new-session -d -s book-generator

# Split the window horizontally
tmux split-window -h -t book-generator

# Start backend server in the left pane
echo -e "${GREEN}Starting Django backend server...${NC}"
tmux send-keys -t book-generator:0.0 "cd /home/badr/book-generator/backend && source venv/bin/activate && python manage.py runserver" C-m

# Start frontend server in the right pane
echo -e "${GREEN}Starting Vue.js frontend server...${NC}"
tmux send-keys -t book-generator:0.1 "cd /home/badr/book-generator/frontend && npm run dev" C-m

# Attach to the tmux session
echo -e "${GREEN}Attaching to tmux session...${NC}"
echo -e "${BLUE}Press Ctrl+B then D to detach from the session${NC}"
tmux attach-session -t book-generator

echo -e "${GREEN}Services restarted successfully!${NC}"