#!/bin/bash

API_URL="http://localhost:5000/api/timeline_post"


echo "Adding endpoint..."
response=$(curl -s -X POST "${API_URL}" -d "name=Maya&email=maya@gmail.com&content=testing2")

sleep 2

verification=$(curl -s "${API_URL}")

print=$(python test.py "${verification}" "${response}")

echo "${print}"
