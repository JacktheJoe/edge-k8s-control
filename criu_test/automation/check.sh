#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <deploymentname>"
    exit 1
fi

deploymentname=$1

# Fetch the namespace, deployment name and IP address
read namespace pod_name ip_address <<< $(kubectl get pods -A -owide | grep $deploymentname | awk '{print $1, $2, $8}')

# Check if anything is set, and exit if trying to access kube-system pods
if [ -z "$pod_name" ] || [ -z "$ip_address" ]; then
    echo "Could not fetch deployment name or IP address."
    exit 1
fi

if [ "$namespace" == "kube-system" ]; then
    echo "Could not modify kube-system components"
    exit 1
fi

# given if the container name is named "<container name>-deployment"
intermediate_name=$(echo $pod_name | awk -F- 'BEGIN {OFS="-"} {NF-=2; print}')
# so that if "-deployment" is present, it is removed
container_name=$(echo $intermediate_name | sed 's/-deployment//')

file_path=$(echo $({ curl -X POST "https://$ip_address:10250/checkpoint/$namespace/$pod_name/$container_name" --insecure --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt --key /etc/kubernetes/pki/apiserver-kubelet-client.key; } 2>&1 | tail -n 1) | sed -e 's/.*\["\(.*\)"\].*/\1/')

filename=$(echo $file_path | awk -F/ '{print $NF}')

echo $ip_address $filename