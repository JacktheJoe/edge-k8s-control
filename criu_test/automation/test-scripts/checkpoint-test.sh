#!/bin/bash

# The IP address of the node running the server
SERVER_IP="10.100.25.10"

# The endpoint to test, now with port 30005
ENDPOINT="http://$SERVER_IP:30005/migration-request"

# Sample migration name to send in the request
MIGRATION_NAME="heartbeat"

# Sample target node name to send in the request
TARGET_NODE_NAME="worker-5-1"

# Make a POST request with curl including the target node name
curl -X POST $ENDPOINT \
     -H "Content-Type: application/json" \
     -d "{\"migration_name\":\"$MIGRATION_NAME\", \"target_node_name\":\"$TARGET_NODE_NAME\"}"
     #-d "{\"migration_name\":\"$MIGRATION_NAME\"}"
