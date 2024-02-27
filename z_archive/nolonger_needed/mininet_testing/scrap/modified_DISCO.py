
import socket
import sys
import threading
import time
import os
import pandas as pd

# Load node metrics from the CSV file
def load_node_metrics(file_path):
    df = pd.read_csv(file_path)
    return {row['Node']: {'Cpu': row['Cpu'], 'Ram': row['Ram']} for index, row in df.iterrows()}

# Define the paths as in the original DISCO.py script
base_path = "/home/jack/Desktop/mininet/DISCO-like"
sending_path = os.path.join(base_path, "sending_outputs")
forwarding_path = os.path.join(base_path, "forwarding_outputs")
receiving_path = os.path.join(base_path, "receiving_outputs")
results_path = os.path.join(base_path, "results")

# Create the subdirectories if they don't exist
os.makedirs(sending_path, exist_ok=True)
os.makedirs(forwarding_path, exist_ok=True)
os.makedirs(receiving_path, exist_ok=True)
os.makedirs(results_path, exist_ok=True)

# Function to write data to files, similar to DISCO.py
def write_to_file(filename, data, output_path):
    full_file_path = os.path.join(output_path, filename)
    with open(full_file_path, "a") as f:
        f.write(data)

# Function to send data to all neighbors
def send_data(node_name, node_ip, metrics, target_ips):
    interval = 10  # send data every 10 seconds
    while True:
        for ip in target_ips:
            if ip != node_ip:  # Don't send to self
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, 9999))
                        data_packet = f"Node: {node_name}, Cpu: {metrics[node_name]['Cpu']}, Ram: {metrics[node_name]['Ram']}"
                        client_socket.send(data_packet.encode())
                        print(f"Sent data to {ip}", flush=True)
                        write_to_file(f"{node_name}.txt", f"Sent data to {ip}: {data_packet}\n", sending_path)
                except ConnectionRefusedError:
                    print(f"Failed to connect to {ip}", flush=True)
        time.sleep(interval)

# Function to handle incoming client connections
def handle_client(client_socket, node_name, metrics, target_ips):
    try:
        data = client_socket.recv(1024)
        decoded_data = data.decode()
        print(f"Received data: {decoded_data}", flush=True)
        write_to_file(f"{node_name}.txt", f"Received data: {decoded_data}\n", receiving_path)

        # Redirect the received data to all other nodes except the sender
        sender_node = decoded_data.split(", ")[0].split(": ")[1]
        for ip in target_ips:
            if ip != sender_node:  # Skip the original sender
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, 9999))
                        client_socket.send(decoded_data.encode())
                        print(f"Redirected data to {ip}", flush=True)
                        write_to_file(f"{node_name}.txt", f"Redirected data to {ip}: {decoded_data}\n", forwarding_path)
                except ConnectionRefusedError:
                    print(f"Failed to redirect to {ip}", flush=True)
    finally:
        client_socket.close()

# Function to start the server
def start_server(port, node_name, metrics, target_ips):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Node {node_name} listening on port {port}", flush=True)

    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr}", flush=True)
        client_handler = threading.Thread(target=handle_client, args=(client, node_name, metrics, target_ips))
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python3 send_receive_node_data.py <node_name> <cpu_usage> <ram_usage> <latency> <bandwidth> <target_ip1> [<target_ip2> ...]", flush=True)
        sys.exit(1)

    node_name, cpu_usage, ram_usage, latency, bandwidth = sys.argv[1:6]
    target_ips = sys.argv[6:]

    # Define node_ip by parsing node_name
    node_ip = f"10.0.0.{int(node_name[1:])}"

    # Load metrics from the CSV file
    metrics = load_node_metrics('/mnt/data/data.csv')

    # Start server thread
    server_thread = threading.Thread(target=start_server, args=(9999, node_name, metrics, target_ips))
    server_thread.start()

    # Start data sending in a separate thread
    send_data_thread = threading.Thread(target=send_data, args=(node_name, node_ip, metrics, target_ips))
    send_data_thread.start()
    