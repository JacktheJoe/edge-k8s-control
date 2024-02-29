import socket
import sys
import threading
import time
import os
import csv

# Set the interval for sending data
interval = 10

# Define the paths as in the original script
base_path = "/home/jack/Desktop/mininet/RAFT-like"
sending_path = os.path.join(base_path, "sending_outputs")
forwarding_path = os.path.join(base_path, "forwarding_outputs")
receiving_path = os.path.join(base_path, "receiving_outputs")
results_path = os.path.join(base_path, "results")
results_node_path = os.path.join(base_path, "results_node")

# Create the subdirectories if they don't exist
os.makedirs(sending_path, exist_ok=True)
os.makedirs(forwarding_path, exist_ok=True)
os.makedirs(receiving_path, exist_ok=True)
os.makedirs(results_path, exist_ok=True)

# Dictionary to store metrics for each neighbor
neighbor_metrics = {}

# Dictionary to store all node's metrics
all_metrics = {}

# Variable to store the lowest utilization and its node name
lowest_utilization = float('inf')
lowest_node_name = ""

# Function to write data to files, similar to DISCO.py
def write_to_file(filename, data, output_path):
    full_file_path = os.path.join(output_path, filename)
    with open(full_file_path, "a") as f:
        f.write(data)

# Function to send data to all neighbors
def send_data(node_name, node_ip, cpu_usage, ram_usage, latency, bandwidth, target_ips, interval):
    while True:
        for ip in target_ips:
            if ip != node_ip:  # Don't send to self
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, 9999))
                        data_packet = f"Type: 1, Node: {node_name}, Cpu: {cpu_usage}, Ram: {ram_usage}, Latency: {latency}, Bandwidth: {bandwidth}"
                        client_socket.send(data_packet.encode())
                        # print(f"Sent data to {ip}", flush=True)
                        write_to_file(f"{node_name}.txt", f"Sent data to {ip}: {data_packet}\n", sending_path)
                except ConnectionRefusedError:
                    print(f"Failed to connect to {ip}", flush=True)
        time.sleep(interval)

# Function to handle incoming client connections
def handle_client(client_socket, node_name, target_ips):
    try:
        data = client_socket.recv(1024)
        decoded_data = data.decode()
        # print(f"Received data: {decoded_data}", flush=True)
        write_to_file(f"{node_name}.txt", f"Received data: {decoded_data}\n", receiving_path)

        # Extract metrics from received data
        metrics = {}
        for item in decoded_data.split(", "):
            key, value = item.split(": ")
            metrics[key] = value

        # Update local record for the neighbor
        neighbor_name = metrics["Node"]
        neighbor_metrics[neighbor_name] = metrics

        # Save local record to a CSV file named after the node
        save_local_record(node_name)

    finally:
        client_socket.close()

# Function to save the local record to a CSV file named after the node
def save_local_record(node_name):
    csv_file = os.path.join(results_path, f"{node_name}.csv")
    
    # Extract the node's own metric
    own_metrics = {
        "Node": node_name,
        "Cpu": cpu_usage,
        "Ram": ram_usage,
        "Latency": latency,
        "Bandwidth": bandwidth
    }

    # Combine local node's metrics with neighbor metrics
    all_metrics = [own_metrics] + list(neighbor_metrics.values())

    sorted_all_metrics = sorted(all_metrics, key=lambda x: x['Node'])

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Node", "Cpu", "Ram", "Latency", "Bandwidth"])

        # Write all metrics to the CSV file
        for metrics in sorted_all_metrics:
            writer.writerow([metrics["Node"], metrics["Cpu"], metrics["Ram"], metrics["Latency"], metrics["Bandwidth"]])

    # Calculate and update the lowest utilization and its node name
    global lowest_utilization
    global lowest_node_name
    lowest_utilization = float('inf')  # Reset to positive infinity
    for metrics in sorted_all_metrics:
        cpu = float(metrics["Cpu"])
        ram = float(metrics["Ram"])
        mean_util = (cpu + ram) / 2

        if mean_util < lowest_utilization:
            lowest_utilization = mean_util
            lowest_node_name = metrics["Node"]

    # Call the function to write the lowest utilization to a local text file
    write_lowest_utilization_to_file(node_name)

# Function to write the lowest utilization and node name to a local text file
def write_lowest_utilization_to_file(node_name):
    output_file = os.path.join(results_node_path, f"{node_name}.txt")

    with open(output_file, mode='w') as file:
        file.write(f"{lowest_node_name}\n")
        file.write(f"{lowest_utilization}")

# Function to start the server
def start_server(port, node_name, target_ips):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    # print(f"Node {node_name} listening on port {port}", flush=True)

    while True:
        client, addr = server_socket.accept()
        # print(f"Accepted connection from {addr}", flush=True)
        client_handler = threading.Thread(target=handle_client, args=(client, node_name, target_ips))
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: data-passing.py node_name cpu_usage ram_usage latency bandwidth neighbor_ip1 [neighbor_ip2 ...]")
        sys.exit(1)

    node_name, cpu_usage, ram_usage, latency, bandwidth = sys.argv[1:6]
    target_ips = sys.argv[6:]

    # Define node_ip by parsing node_name
    node_ip = f"10.0.0.{int(node_name[1:])}"

    # Start server thread
    server_thread = threading.Thread(target=start_server, args=(9999, node_name, target_ips))
    server_thread.start()

    # Start data sending in a separate thread with the interval
    send_data_thread = threading.Thread(target=send_data, args=(node_name, node_ip, cpu_usage, ram_usage, latency, bandwidth, target_ips, interval))
    send_data_thread.start()

    # Fetch and write lowest utilization to a local text file
    write_lowest_utilization_to_file(node_name)

# Access lowest utilization value and node name in other parts of the code if needed
# print(f"Lowest Utilization Node: {lowest_node_name}")
# print(f"Lowest Utilization Value: {lowest_utilization}")