#!/bin/bash

# associated pair of subnets and update URL
declare -A all_clusters
all_clusters=(["10.200.31.0/24"]="http://10.200.31.10:30001" ["10.200.32.0/24"]="http://10.200.32.10:30001" ["10.200.33.0/24"]="http://10.200.33.10:30001") 

# PING_TARGET="1.1.1.1"
PING_TARGET="10.200.30.10"
NUM_PING="1"
log_server="http://10.200.30.10:20000"

get_basic_reading(){
	kubectl top nodes | grep worker | awk {'first = $1; $1=""; print $0'} | sed 's/^ //g'
}

get_average(){
	grep -o '[0-9]\+' | awk 'a+=$1/2; END{print a}' | awk -F: 'NR==3 {print $1}'
}

get_time_reading(){
	date +"%Y-%m-%d %T"
}

get_ping_result(){
	ping -c $NUM_PING $PING_TARGET | grep from | awk '{for (i=6; i<=NF-1; i++) print $i}'
}

ping_average(){
	awk 'a+=$1/$NUM_PING; END{print a}' | awk -F: 'NR==$NUM_PING {print $1}'
}

round_number(){
	awk '{for (i=1; i<=NF; i++) printf "%.3f %s", $i, (i==NF?"\n":" ")}'
}

iperf_result(){
	iperf3 -s -i 2 -p 5201
}

external_ip(){
	# updated to using external node's IP variable
	subnet=$(echo "$NODE_IP" | awk 'BEGIN{FS=OFS="."}{NF--; print $0}')
	subnet="${subnet}.0/24"
	echo $subnet
}

monitoring(){
	# metric server
	basic_metric_reading=$(get_basic_reading)
	cpu_num_reading=$(echo "$basic_metric_reading" | awk '{ print $1 }' | get_average)
	ram_num_reading=$(echo "$basic_metric_reading" | awk '{ print $3 }' | get_average)
	cpu_per_calculating=$(echo "$basic_metric_reading" | awk '{ print $2 }' | get_average)
	ram_per_reading=$(echo "$basic_metric_reading" | awk '{ print $4 }' | get_average)

node_index=1
result_json="{}"

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

	# ping, tried to return multiple numbers from function but bash can only return integers
	filter_ttl=$(get_ping_result | grep "ttl" | awk -F '=' '{print $2}' | ping_average)
	filter_time=$(get_ping_result | grep "time" | awk -F '=' '{print $2}' | ping_average | round_number)
	
	# process subnet information from node's IP
	# subnet=$(hostname -I | awk '{print $1}' | awk 'BEGIN{FS=OFS="."}{NF--; print}') 
	
	subnet=$(external_ip)

	if test -z "$cpu_per_calculating" 
	then
    	cpu_per_reading=0
	else
    	cpu_per_reading=$cpu_per_calculating
	fi

	JSON_STRING=$( jq -n \
				  --arg x "$subnet" \
				  --arg y "$(get_time_reading)" \
                  --arg b "$cpu_num_reading" \
                  --arg c "$ram_num_reading" \
				  --arg d "$cpu_per_reading" \
				  --arg e "$ram_per_reading" \
				  --arg f "$filter_ttl" \
				  --arg g "$filter_time" \
				  --argjson per_node "$result_json" \
				  '{subnet: $x, time: $y, data: {general: {mili_CPU: $b, Mi_RAM: $c, percent_CPU: $d, percent_RAM: $e, ping_ttl: $f, ping_time: $g}, detail: $per_node}}')
	echo $JSON_STRING
}

send_json_post(){
	send_data=$(monitoring)
	curl -X POST -H 'Content-Type: application/json' --data "$send_data" $log_server
	#echo "$send_data" > /code/outputs/local_machine/localmetrics.json
	for key in "${!all_clusters[@]}"; do
		curl -X POST -H 'Content-Type: application/json' --data "$send_data" ${all_clusters[$key]}
	done
}

prep(){
	if [[ ! -e /code/deployment/ ]]; then
    	mkdir -p /code/deployment/
	fi

	# if [[ ! -e /code/outputs/local_machine/ ]]; then
    # 	mkdir -p /code/outputs/local_machine/
	# fi

	#if [[ ${all_clusters["$(external_ip)"]} ]]; then
    #	unset 'all_clusters["$(external_ip)"]'
	#fi
}

prep

while true
do
	send_json_post > /dev/null 2>&1
	sleep 5
done