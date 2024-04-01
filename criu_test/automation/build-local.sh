#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No filename provided"
    exit 1
fi

filename=$1

chmod 777 $filename

cat <<EOF > Dockerfile
FROM scratch
ADD $filename .
EOF

time_string=$(date +%Y%m%d%H%M%S)
deploymentbase=$(echo $filename | cut -d'_' -f1 | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]-')
deploymentname="${deploymentbase}-restore-${time_string}"

buildah bud --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=$deploymentname -t $deploymentname:latest Dockerfile . 2>&1 | tee -a build_output.txt
# buildah push 

rm -f Dockerfile

echo $deploymentname
