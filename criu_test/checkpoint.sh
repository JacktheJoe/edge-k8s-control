#!/bin/bash

# Fetch the deployment name and node name
read full_deployment_name node_indicator <<< $(kubectl get pods -owide | awk 'NR==2 {print $1, $9}')

# Process the deployment name to extract the required part
deployment_name=$(echo $full_deployment_name | sed 's/-[a-z0-9]*-[a-z0-9]*$//')

# Check if the variables are set
if [ -z "$deployment_name" ] || [ -z "$node_indicator" ]; then
    echo "Could not fetch deployment name or node name."
    exit 1
fi

# Execute the curl command and include the output of 'time'
{ time curl -X POST "https://$node_indicator:10250/checkpoint/default/$full_deployment_name/$deployment_name" \
    --insecure \
    --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt \
    --key /etc/kubernetes/pki/apiserver-kubelet-client.key; } 2>&1 | tee /home/jack/output.txt

