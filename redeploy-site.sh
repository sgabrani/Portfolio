#!/bin/bash
cd /root/Portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio
<<comment
# Step 1: Kill all existing tmux sessions
tmux kill-server

# Step 2: Change directory to your project folder
cd Portfolio/

# Step 3: Fetch the latest changes from GitHub and reset the local repository
git fetch && git reset origin/main --hard

# Step 4: Enter the Python virtual environment and install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Step 5: Start a new detached Tmux session and run the Flask server
tmux new-session -d 'flask run --host=0.0.0.0'
comment
