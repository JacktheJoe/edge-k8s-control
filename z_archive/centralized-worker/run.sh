#!/bin/bash

# start iperf server
iperf3 -s -p 5201 &
# start peer metric receive
uvicorn peer-update:app --reload --host 0.0.0.0 --port 8080 &
# start consense listening
uvicorn consensus:app --reload --host 0.0.0.0 --port 10000 &
# start deployment yaml receive
uvicorn receive-deployment:app --reload --host 0.0.0.0 --port 8081 &
# send metric update
bash update.sh &

sleep infinity
