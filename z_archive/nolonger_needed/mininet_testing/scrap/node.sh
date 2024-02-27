#!/bin/bash

# Get the directory of the current script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Full path to the CSV files
data_csv="$script_dir/data.csv"
network_csv="$script_dir/network.csv"

# Extract the interface name from the third line of the route command's output
interface_name=$(route | awk 'NR==3 {print $8}')

# Extract the node name from the interface name
node_name=$(echo $interface_name | cut -d'-' -f1)

# Find the corresponding CPU and RAM usage from data_csv
cpu_ram_usage=$(awk -F, -v node="$node_name" '$1 == node {print $2" "$3}' "$data_csv")
cpu_usage=$(echo $cpu_ram_usage | cut -d' ' -f1)
ram_usage=$(echo $cpu_ram_usage | cut -d' ' -f2)

# Find the corresponding Latency and Bandwidth from network_csv
latency_bandwidth=$(awk -F, -v node="$node_name" '$1 == node {print $2" "$3}' "$network_csv")
latency=$(echo $latency_bandwidth | cut -d' ' -f1)
bandwidth=$(echo $latency_bandwidth | cut -d' ' -f2)

# Define the full range of IPs
full_ips=("10.0.0."{1..9})

# Remove the node's own IP from the list to get the neighbors' IPs
neighbor_ips_array=()
for ip in "${full_ips[@]}"; do
    if [[ $ip != "10.0.0.${node_name:1}" ]]; then
        neighbor_ips_array+=("$ip")
    fi
done

# Add the last IP (10.0.0.9) to the neighbors
neighbor_ips_array+=("10.0.0.9")

# for RAFT-like
#python3 "$script_dir/data-passing.py" "$node_name" "$cpu_usage" "$ram_usage" "$latency" "$bandwidth" "${neighbor_ips_array[@]}" || {
#    echo "Error: data-passing.py failed to execute."
#    exit 1
#}

python3 "$script_dir/data-passing.py" "$node_name" "$cpu_usage" "$ram_usage" "$latency" "$bandwidth" "${neighbor_ips_array[@]}" &

# sleep 2
# python3 "$script_dir/raft.py" &

python3 "$script_dir/ip_process.py" "$node_name" "10.0.0.${node_name:1}" "${neighbor_ips_array[@]}" "8080" &

echo "Node name: $node_name"
echo "Node IP: 10.0.0.${node_name:1}"
echo "CPU Usage: $cpu_usage%"
echo "RAM Usage: $ram_usage%"
echo "Latency: $latency ms"
echo "Bandwidth: $bandwidth Mbps"

# Print out neighbors
echo "Neighbors:"
for ip in "${neighbor_ips_array[@]}"; do
    echo "$ip"
done

wait
