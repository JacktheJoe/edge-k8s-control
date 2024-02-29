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

# Extract direct connected neighbor IPs from the route command and store them in an array
neighbor_ips_array=($(route -n | awk 'NR>3 && $1 != "0.0.0.0" && $1 != "Destination" {print $1}'))

# for DISCO-like
# python3 "$script_dir/send_receive_node_data.py" "$node_name" "$cpu_usage" "$ram_usage" "$latency" "$bandwidth" "${neighbor_ips_array[@]}"
python3 "$script_dir/DISCO.py" "$node_name" "$cpu_usage" "$ram_usage" "$latency" "$bandwidth" "${neighbor_ips_array[@]}"

echo "Node name: $node_name"
echo "CPU Usage: $cpu_usage%"
echo "RAM Usage: $ram_usage%"
echo "Latency: $latency ms"
echo "Bandwidth: $bandwidth Mbps"

echo "Neighbor_IPs: "
# Print all neighbor IPs using echo
for ip in "${neighbor_ips_array[@]}"; do
    echo "    $ip"
done