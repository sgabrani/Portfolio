#!/bin/bash

# Step 1: Change directory to your project folder
cd /Portfolio

# Step 2: Fetch the latest changes from the main branch on GitHub
git fetch && git reset origin/main --hard

# Step 3: Spin containers down to prevent out of memory issues
docker-compose -f docker-compose.prod.yml down

# Step 4: Build and bring up the containers
docker-compose -f docker-compose.prod.yml up -d --build
