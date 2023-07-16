#!/bin/bash

# Change directory to project folder
cd ./Portfolio

# Fetch latest changes from main branch on GitHub and reset local repository
git fetch && git reset origin/main --hard

# Activate Python virtual environment and install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Restart myportfolio service
systemctl daemon-reload
systemctl restart myportfolio