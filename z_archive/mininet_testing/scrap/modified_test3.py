import socket
import sys
import threading
import time
import os

# Define the max_hop value
max_hop = 2

# Define the time interval
time_interval = 10  # 5 minutes in seconds

# Define the base path
base_path = "/home/jack/Desktop/mininet/3x3"

# Define the output subdirectories
sending_path = os.path.join(base_path, "sending_outputs")
forwarding_path = os.path.join(base_path, "forwarding_outputs")
receiving_path = os.path.join(base_path, "receiving_outputs")
results_path = os.path.join(base_path, "results")

# Create the subdirectories if they don't exist
os.makedirs(sending_path, exist_ok=True)
os.makedirs(forwarding_path, exist_ok=True)
os.makedirs(receiving_path, exist_ok=True)
os.makedirs(results_path, exist_ok=True)

# Global dictionary to store the matrix of metrics
metrics_matrix = {}

def write_to_file(filename, data, output_path):
    full_file_path = os.path.join(output_path, filename)
    with open(full_file_path, "a") as f:
        f.write(data)

def write_empty_lines(node_name, output_path):
    # Create empty lines
    empty_lines = "\n" * 3

    # Write empty lines to the node_name.txt file in the specified directory
    filename = f"{node_name}.txt"
    full_file_path = os.path.join(output_path, filename)
    
    with open(full_file_path, "a") as f:
        f.write(empty_lines)

def ip_to_name(ip_address):
    try:
        last_segment = ip_address.split('.')[-1]
        return f"h{int(last_segment)}"
    except (IndexError, ValueError):
        return "Invalid IP"

def calculate_and_write_lowest_avg_metrics(node_name):
    end_time = time.time()  # Capture the time when the result is determined
    result_full_path = os.path.join(results_path, f"{node_name}.txt")

    lowest_avg = None
    lowest_sender_name = None

    for sender_id, metrics in metrics_matrix.items():
        try:
            avg = (float(metrics['CPU']) + float(metrics['RAM'])) / 2
            duration = end_time - start_time  # Calculate the duration
            if lowest_avg is None or avg < lowest_avg:
                lowest_avg = avg
                lowest_sender_name = ip_to_name(sender_id)
            print(f'Time taken: {duration} seconds')  # Print the time taken
        except ValueError:
            continue

    if lowest_sender_name is not None:
        data = f"Offload target: {lowest_sender_name}, Average: {lowest_avg}\n"
        write_to_file(result_full_path, data, results_path)

def update_metrics_matrix(node_name, sender_id, cpu, ram, latency, bandwidth):
    metrics_matrix[sender_id] = {
        'CPU': cpu,
        'RAM': ram,
        'Latency': latency,
        'Bandwidth': bandwidth
    }
    calculate_and_write_lowest_avg_metrics(node_name)

def handle_client(client_socket, node_name):
    try:
        data = client_socket.recv(1024)
        decoded_data = data.decode()
        print(f"Received data: {decoded_data}", flush=True)
        
        write_to_file(f"{node_name}.txt", f"Received data: {decoded_data}\n", receiving_path)

        parts = decoded_data.split(", ")
        sender_id = None
        cpu_usage = None
        ram_usage = None
        latency = None
        bandwidth = None

        for part in parts:
            if part.startswith("Current_Hop: "):
                current_hop = int(part[len("Current_Hop: "):])
            elif part.startswith("Receiver_ID: "):
                receiver_id = part[len("Receiver_ID: "):]
            elif part.startswith("Sender_ID: "):
                sender_id = part[len("Sender_ID: "):]
            elif part.startswith("CPU: "):
                cpu_usage = part[len("CPU: "):]
            elif part.startswith("RAM: "):
                ram_usage = part[len("RAM: "):]
            elif part.startswith("Latency: "):
                latency = part[len("Latency: "):]
            elif part.startswith("Bandwidth: "):
                bandwidth = part[len("Bandwidth: "):]
        
        # If the message needs forwarding and current_hop is greater than 0, forward to neighbors
        if current_hop is not None and current_hop > 0:
            forward_message(decoded_data, current_hop, sender_id, receiver_id, node_name)

        if sender_id:
            update_metrics_matrix(node_name, sender_id, cpu_usage, ram_usage, latency, bandwidth)

    finally:
        client_socket.close()

def forward_message(data, current_hop, sender_id, receiver_id, node_name):
    # Decrement current_hop before forwarding
    hop_count = current_hop - 1

    if hop_count < 1:
        return  # Stop forwarding when current_hop is less than 1
    
    # Define node_ip by parsing node_name
    node_ip = f"10.0.0.{int(node_name[1:])}"
    
    for ip in target_ips:
        if ip != node_ip and ip != receiver_id and ip != sender_id:  # Skip forwarding to the original sender and the neighbor who sent the message
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, 9999))
                    data_packet = data.replace(f"Receiver_ID: {receiver_id}", f"Receiver_ID: {ip}")
                    data_packet = data_packet.replace(f"Current_Hop: {current_hop}", f"Current_Hop: {hop_count}")
                    client_socket.send(data_packet.encode())
                    print(f"Forwarded data to {ip}", flush=True)

                    # Write the forwarded data to a file in the forwarding_outputs directory
                    write_to_file(f"{node_name}.txt", f"Forwarded data to {ip}: {data_packet}\n", forwarding_path)
                    
            except ConnectionRefusedError:
                print(f"Failed to connect to {ip}", flush=True)

def start_server(port, node_name):
    global start_time  # Define a global variable to store the start time
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Node {node_name} listening on port {port}", flush=True)

    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr}", flush=True)
        client_handler = threading.Thread(target=handle_client, args=(client, node_name))
        client_handler.start()

def send_data(node_name, node_ip, cpu_usage, ram_usage, latency, bandwidth, target_ips):
    while True:
        current_hop = max_hop

        for ip in target_ips:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((ip, 9999))
                    data_packet = f"Type: 1, Current_Hop: {current_hop}, Max_Hop: {max_hop}, Sender_ID: {node_ip}, Receiver_ID: {ip}, CPU: {cpu_usage}, RAM: {ram_usage}, Latency: {latency}, Bandwidth: {bandwidth}"
                    client_socket.send(data_packet.encode())
                    print(f"Sent data to {ip}", flush=True)
                    
                    # Write the sent data to a file in the sending_outputs directory
                    write_to_file(f"{node_name}.txt", f"Sent data to {ip}: {data_packet}\n", sending_path)
                    
            except ConnectionRefusedError:
                print(f"Failed to connect to {ip}", flush=True)

        # Write empty lines to the sending_outputs file
        write_empty_lines(node_name, sending_path)
        
        print("Sent data to all neighbors. Waiting for the next iteration...", flush=True)
        time.sleep(time_interval)  # Wait for the specified time interval

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: python3 send_receive_node_data.py <node_name> <cpu_usage> <ram_usage> <latency> <bandwidth> <target_ip1> [<target_ip2> ...]", flush=True)
        sys.exit(1)

    node_name, cpu_usage, ram_usage, latency, bandwidth = sys.argv[1:6]
    target_ips = sys.argv[6:]

    # Define node_ip by parsing node_name
    node_ip = f"10.0.0.{int(node_name[1:])}"
    
    # Start server thread
    server_thread = threading.Thread(target=start_server, args=(9999, node_name))
    server_thread.start()

    # Send data in a separate thread
    send_data_thread = threading.Thread(target=send_data, args=(node_name, node_ip, cpu_usage, ram_usage, latency, bandwidth, target_ips))
    send_data_thread.start()
    
    # Add a sleep here to keep the main thread running
    while True:
        time.sleep(1)