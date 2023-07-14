#!/bin/bash

# GET
curl http://127.0.0.1:5000/api/timeline_post

# POST
curl -X POST http://127.0.0.1:5000/api/timeline_post -d 'name=Aparna&email=aparnaroy@mlh.com&content=Testing my endpoints with curl.'

# GET
curl http://127.0.0.1:5000/api/timeline_post