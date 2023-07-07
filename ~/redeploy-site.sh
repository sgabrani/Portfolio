#!/bin/bash

# Kill all existing tmux sessions
tmux list-sessions | grep -v attached | awk 'BEGIN{FS=":"}{print $1}' | xargs -n 1 tmux kill-session -t || echo No sessions to kill

# Change directory to your project folder
cd ./Portfolio

# Fetch the latest changes from the main branch on GitHub and reset the local repository
git fetch && git reset origin/main --hard

# Activate the Python virtual environment and install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start a new detached Tmux session and run the Flask server
tmux new-session -d -s MyPortfolio
tmux send-keys "cd ./Portfolio" C-m
tmux send-keys "source python3-virtualenv/bin/activate" C-m
tmux send-keys "flask run --host=0.0.0.0" C-m