#!/bin/sh

# updates and constructs resource metric in JSON format

file_path=$METRIC_LOG

# Define the all_clusters array
#declare -A all_clusters
#
# Iterate over the environment variables (set in Dockerfile)
#for var in $(env | grep '^CLUSTER_[0-9]*_SUBNET='); do
#    subnet_var=$(echo "$var" | cut -d= -f1)
#    url_var=$(echo "$subnet_var" | sed 's/SUBNET/URL/')
#    subnet="${!subnet_var}"
#    url="${!url_var}"
#    cluster_number=$(echo "$subnet_var" | sed 's/CLUSTER_\([0-9]*\)_SUBNET/\1/')
#    all_clusters["$subnet"]="$url"
#done

log_server="http://${DATA_SERVER_IP}:${DATA_SERVER_PORT}"

get_basic_reading(){
	kubectl top nodes | grep worker | awk {'first = $1; $1=""; print $0'} | sed 's/^ //g'
}

get_average(){
	grep -o '[0-9]\+' | awk 'a+=$1/2; END{print a}' | awk -F: 'NR==3 {print $1}'
}

get_time_reading(){
	date +"%Y-%m-%d %T"
}

#external_ip(){
#	# updated to using external node's IP variable (local cluster)
#	subnet=$(echo "$NODE_IP" | awk 'BEGIN{FS=OFS="."}{NF--; print $0}')
#	subnet="${subnet}.0/24"
#	echo $subnet
#}
#
#subnet=$(external_ip)
## make sure nothing gets send to self
#unset all_clusters["$subnet"]

monitoring(){
	# fetch the average load on workers from metric API
	basic_metric_reading=$(get_basic_reading)
	cpu_num_reading=$(echo "$basic_metric_reading" | awk '{ print $1 }' | get_average)
	ram_num_reading=$(echo "$basic_metric_reading" | awk '{ print $3 }' | get_average)
	cpu_per_calculating=$(echo "$basic_metric_reading" | awk '{ print $2 }' | get_average)
	ram_per_reading=$(echo "$basic_metric_reading" | awk '{ print $4 }' | get_average)

node_index=1
result_json="{}"

# to extract per_node metrics for each worker nodes
while IFS=" " read -r mili_CPU percent_CPU Mi_RAM percent_RAM; do
    # Extracting only numbers from the metric readings
    mili_CPU=$(echo "$mili_CPU" | grep -o '[0-9]\+')
    percent_CPU=$(echo "$percent_CPU" | grep -o '[0-9]\+')
    Mi_RAM=$(echo "$Mi_RAM" | grep -o '[0-9]\+')
    percent_RAM=$(echo "$percent_RAM" | grep -o '[0-9]\+')

    current_json=$(jq -n \
    --arg node "node_${node_index}" \
    --arg mili_CPU "$mili_CPU" \
    --arg percent_CPU "$percent_CPU" \
    --arg Mi_RAM "$Mi_RAM" \
    --arg percent_RAM "$percent_RAM" \
    '{($node): {"mili_CPU": $mili_CPU, "Mi_RAM": $Mi_RAM, "percent_CPU": $percent_CPU, "percent_RAM": $percent_RAM}}')

    result_json=$(jq --argjson current "$current_json" '. += $current' <<< "$result_json")
    ((node_index++))
done <<< "$basic_metric_reading"

	if test -z "$cpu_per_calculating" 
	then
    	cpu_per_reading=0
	else
    	cpu_per_reading=$cpu_per_calculating
	fi

    JSON_STRING=$( jq -n \
				  --arg a "$subnet" \
				  --arg b "$(get_time_reading)" \
				  --arg c "$CPU_CORE_PT" \
                  --arg d "$CPU_CORECOUNT" \
                  --arg e "$cpu_num_reading" \
                  --arg f "$ram_num_reading" \
				  --arg g "$cpu_per_reading" \
				  --arg h "$ram_per_reading" \
				  --argjson per_node "$result_json" \
				  '{subnet: $a, time: $b, data: {general: {cpu_score_pt: $c, cpu_corecount: $d, mili_CPU: $e, Mi_RAM: $f, percent_CPU: $g, percent_RAM: $h}, detail: $per_node}}')
	echo $JSON_STRING
}

send_json_post(){
	send_data=$(monitoring)
	curl -X POST -H 'Content-Type: application/json' --data "$send_data" $log_server
	#echo "$send_data" > /code/outputs/local_machine/localmetrics.json
	#for key in "${!all_clusters[@]}"; do
	#	curl -X POST -H 'Content-Type: application/json' --data "$send_data" ${all_clusters[$key]}
	#done
	curl -X POST -H 'Content-Type: application/json' --data "$send_data" http://localhost:8002
	echo "$JSON_STRING" > "$file_path"
}

# Check if the file exists
if [ -f "$file_path" ]; then
    # Empty the file
    > "$file_path"
fi

while true
do
	send_json_post > /dev/null 2>&1
	sleep $UPDATE_INTERVAL
done