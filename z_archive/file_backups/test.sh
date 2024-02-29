#!/bin/bash

SAVE_LOCATION="/home/jack/metrics/outputs"
PING_TARGET="1.1.1.1"
NUM_PING="3"
log_server="http://10.200.30.10:20000"

if [[ ! -e $SAVE_LOCATION ]]; then
    mkdir $SAVE_LOCATION
fi

# no longer needed - overwriting file anyway
# if [[ -e $SAVE_LOCATION/output.json ]]; then
#     rm $SAVE_LOCATION/output.json
# fi

get_basic_reading(){
	sudo kubectl top nodes | grep worker | awk {'first = $1; $1=""; print $0'} | sed 's/^ //g'
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

average_3(){
	awk 'a+=$1/$NUM_PING; END{print a}' | awk -F: 'NR==3 {print $1}'
}

round_number(){
	awk '{for (i=1; i<=NF; i++) printf "%.3f %s", $i, (i==NF?"\n":" ")}'
}

monitoring(){
	# metric server
	cpu_num_reading=$(get_basic_reading | awk '{ print $1 }' | get_average)
	ram_num_reading=$(get_basic_reading | awk '{ print $3 }' | get_average)
	cpu_per_calculating=$(get_basic_reading | awk '{ print $2 }' | get_average)
	ram_per_reading=$(get_basic_reading | awk '{ print $4 }' | get_average)

	# ping
	filter_ttl=$(get_ping_result | grep "ttl" | awk -F '=' '{print $2}' | average_3)
	filter_time=$(get_ping_result | grep "time" | awk -F '=' '{print $2}' | average_3 | round_number)
	
	# process subnet information from node's IP
	subnet=$(hostname -I | awk '{print $1}' | awk 'BEGIN{FS=OFS="."}{NF--; print}')
	subnet="${subnet}.0/24"

	if test -z "$cpu_per_calculating" 
	then
    	cpu_per_reading=0
	else
    	cpu_per_reading=$cpu_per_calculating
	fi

	# append to file__ changing from txt to json for post

	# printf "$(get_time_reading) \n \
	# Reading in num of milli CPU: \n\t$cpu_num_reading \n \
	# Reading in num of Mi RAM: \n\t$ram_num_reading \n \
	# Reading in percent CPU: \n\t$cpu_per_reading \n \
	# Reading in percent RAM: \n\t$ram_per_reading \n \
	# Reading in ping ttl and ms: \n\t$filter_ttl \n\t$filter_time\n" \
	# >> "$SAVE_LOCATION/output.txt"

	JSON_STRING=$( jq -n \
				  --arg x "$subnet" \
				  --arg y "$(get_time_reading)" \
                  --arg b "$cpu_num_reading" \
                  --arg c "$ram_num_reading" \
				  --arg d "$cpu_per_reading" \
				  --arg e "$ram_per_reading" \
				  --arg f "$filter_ttl" \
				  --arg g "$filter_time" \
				  '{subnet: $x, time: $y, data: {mili_CPU: $b, Mi_RAM: $c, percent_CPU: $d, percent_RAM: $e, ping_ttl: $f, ping_time: $g}}')
	
	echo $JSON_STRING

	# not writting anymore, just send
	# echo $JSON_STRING > $SAVE_LOCATION/output.json
}

send_json_post(){
	curl -X POST -H 'Content-Type: application/json' --data "$(monitoring)" $log_server
}

while true
do
	send_json_post
	sleep 300
done