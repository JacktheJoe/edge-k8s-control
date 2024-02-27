#!/bin/sh

# updates and constructs network metric in JSON format

## Define the all_clusters array
#declare -A all_clusters
#
## Iterate over the environment variables (set in Dockerfile)
#for var in $(env | grep '^CLUSTER_[0-9]*_SUBNET='); do
#    subnet_var=$(echo "$var" | cut -d= -f1)
#    url_var=$(echo "$subnet_var" | sed 's/SUBNET/URL/')
#    subnet="${!subnet_var}"
#    url="${!url_var}"
#    cluster_number=$(echo "$subnet_var" | sed 's/CLUSTER_\([0-9]*\)_SUBNET/\1/')
#    all_clusters["$subnet"]="$url"
#done

log_server="http://${DATA_SERVER_IP}:${DATA_SERVER_PORT}"

#external_ip(){
#	# updated to using external node's IP variable (local cluster)
#	subnet=$(echo "$NODE_IP" | awk 'BEGIN{FS=OFS="."}{NF--; print $0}')
#	subnet="${subnet}.0/24"
#	echo $subnet
#}

#subnet=$(external_ip)
#unset all_clusters["$subnet"]

get_iperf_reading(){
    iperf -c $IPERF_SERVER_IP -p $IPERF_SERVER_PORT -t 10 -y C
}
