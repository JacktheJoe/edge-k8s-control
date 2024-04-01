#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <podname> <originalname>"
    exit 1
fi

podname=$1
originalname=$2

node=$(kubectl get pods -o wide | grep $originalname | awk '{print $7}')

if [ "$node" == "worker-5-1" ] then
    destination_node="worker-5-2"
elif [ "$node" == "worker-5-2" ] then
    destination_node="worker-5-1"
else
    echo "Node not recognized. Exiting."
    exit 1
fi

cat <<EOF > "${podname}-restore.yaml"
---
apiVersion: v1
kind: Pod
metadata:
  name: $podname
  labels:
    app: $podname
spec:
  containers:
  - name: $podname
    image: localhost/$podname:latest
  nodeName: $destination_node
EOF

time kubectl apply -f "${podname}-restore.yaml" 2>&1 | tee -a restore-output.txt

# rm -f "${podname}-restore.yaml"
