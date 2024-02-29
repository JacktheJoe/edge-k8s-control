import socket
import os
import threading
import csv
import time

metric_update_receive_port = os.environ.get('METRIC_UPDATE_RECEIVE_PORT')
metriclog = os.environ.get('METRIC_LOG')

local_url = os.environ.get('NODE_IP')
cluster_name = os.environ.get('NODE_NAME')
subnet_id = os.environ.get('SUBNET')
peer_update_port = int(os.environ.get('PEER_UPDATE_PORT'))

# get all cluster_urls from Dockerfile ENV
def get_neighbor_urls():
    cluster_urls = []
    # Iterate over all environment variables
    for key, value in os.environ.items():
        
        # Check if the environment variable is a cluster URL
        # chahnged ENV from Dockerfile to remove http://
        #if key.startswith("CLUSTER_") and key.endswith("_URL"):
        #    if value.replace("http://", "") != local_url:
        #        cluster_urls.append(value)
        
        if key.startswith("CLUSTER_") and key.endswith("_URL"):
            if value != local_url:
                cluster_urls.append(value)
    return cluster_urls

def handle_client(client_socket, node_name):
    try:
        data = client_socket.recv(1024)
        decoded_data = data.decode()
        print(f"Received data: {decoded_data}", flush=True)
        
        parts = decoded_data.split(", ")
        cpu_amount, cpu_percentage, ram_amount, ram_percentage= None

        for part in parts:
            if part.startswith("Current_Hop: "):
                current_hop = int(part[len("Current_Hop: "):])
            elif part.startswith("Receiver_ID: "):
                receiver_id = part[len("Receiver_ID: "):]
            elif part.startswith("Sender_ID: "):
                sender_id = part[len("Sender_ID: "):]
            elif part.startswith("CPU_amount: "):
                cpu_amount = part[len("CPU_amount: "):]
            elif part.startswith("CPU_percentage: "):
                cpu_percentage = part[len("CPU_percentage: "):]
            elif part.startswith("RAM_amount: "):
                ram_amount = part[len("RAM_amount: "):]
            elif part.startswith("RAM_percentage: "):
                ram_percentage = part[len("RAM_percentage: "):]

        # If the message needs forwarding and current_hop is greater than 0, forward to neighbors
        if current_hop is not None and current_hop > 0:
            forward_message(decoded_data, current_hop, sender_id, receiver_id, node_name)

        if sender_id:
            update_metric(node_name, sender_id, cpu_amount, cpu_percentage, ram_amount, ram_percentage)

    finally:
        client_socket.close()

def forward_message(data, current_hop, sender_id, receiver_id, node_name):
    target_ips = get_neighbor_urls()
    # Decrement current_hop before forwarding
    hop_count = current_hop - 1

    if hop_count < 1:
        return  # Stop forwarding when current_hop is less than 1
    
    for ip in target_ips:
        if ip != local_url and ip != receiver_id and ip != sender_id:  # Skip forwarding to the original sender and the neighbor who sent the message
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, peer_update_port))
                    data_packet = data.replace(f"Receiver_ID: {receiver_id}", f"Receiver_ID: {ip}")
                    data_packet = data_packet.replace(f"Current_Hop: {current_hop}", f"Current_Hop: {hop_count}")
                    client_socket.send(data_packet.encode())
                    print(f"Forwarded data to {ip}", flush=True)
                    
            except ConnectionRefusedError:
                print(f"Failed to connect to {ip}", flush=True)

def update_metric(cluster_id, cpu_core, cpu_percentage, mem_amount, mem_percentage):
    rows = []
    
    # Try reading the existing content and update
    try:
        with open(metriclog, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == cluster_id:
                    rows.append([cluster_id, cpu_core, cpu_percentage, mem_amount, mem_percentage])
                else:
                    rows.append(row)
    except FileNotFoundError:
        pass
    # Sort rows by cluster_id
    rows.sort(key=lambda x: int(x[0].split('_')[-1]))
    # Write the updated content back
    with open(metriclog, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def start_server(port, node_name):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Node {node_name} listening on port {port}", flush=True)

    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr}", flush=True)
        client_handler = threading.Thread(target=handle_client, args=(client, node_name))
        client_handler.start()
        
if __name__ == "__main__":
    
    server_thread = threading.Thread(target=start_server, args=(peer_update_port, cluster_name))
    server_thread.start()
    
    # Add a sleep here to keep the main thread running
    while True:
        time.sleep(1)