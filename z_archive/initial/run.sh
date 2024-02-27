#!/bin/bash

bash update.sh &
uvicorn peer-update:app --reload --host 0.0.0.0 --port 8080 &
uvicorn receive-deployment:app --reload --host 0.0.0.0 --port 8081 &

sleep infinity
