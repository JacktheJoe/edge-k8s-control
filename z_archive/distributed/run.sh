#!/bin/bash

iperf -s -i 5 -p $IPERF_SERVER_PORT &
bash update.sh &
uvicorn peer-update:app --reload --host 0.0.0.0 --port $METRIC_UPDATE_PORT &
uvicorn receive-deployment:app --reload --host 0.0.0.0 --port $DEPLOYMENT_RECEIVE_PORT &

sleep infinity
