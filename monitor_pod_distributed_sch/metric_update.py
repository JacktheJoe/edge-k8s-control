import os
import subprocess
import re
import csv
import socket
import threading
import time

networklog = os.environ.get('NETWORK_LOG')
metriclog = os.environ.get('LOCAL_METRIC_LOG')
decisionlog = os.environ.get('DECISION_LOG')
deploymentlog = os.environ.get('DEPLOYMENT_LOG')

local_url = os.environ.get('NODE_IP')
cluster_name = os.environ.get('NODE_NAME')
subnet_id = os.environ.get('SUBNET')
peer_update_port = int(os.environ.get('PEER_UPDATE_PORT'))

network_interval = int(os.environ.get('NETWORK_INTERVAL'))
peer_update_interval = int(os.environ.get('PEER_UPDATE_INTERVAL'))

max_hop = 2

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

class Resource_matric_fetcher:
    # basically run bash script to call kubectl top nodes
    def fetch_metric_server():
        metric_command = ["kubectl", "top", "nodes"]
        return subprocess.run(metric_command, capture_output=True, text=True)
    
    # processes the fetched data
    def filter_metric_result():
        worker_cpu_percentage = []
        worker_mem_percentage = []
        worker_cpu_core = []
        worker_mem_amount = []
        # since the num of worker and masters are unknown, need to filter out the non-worker nodes from stdout
        lines = [line for line in Resource_matric_fetcher.fetch_metric_server().stdout.strip().split('\n') if "worker" in line]
        if len(lines) == 0:
            return "No worker nodes? Stderr? "
        for line in lines:
            if line:
                line = line.split()
                # split line, filter out non-numeric values and append to corresponding list
                worker_cpu_core.append("".join(re.findall(r"[0-9.]+", line[1])))
                worker_cpu_percentage.append("".join(re.findall(r"[0-9.]+", line[2])))
                worker_mem_amount.append("".join(re.findall(r"[0-9.]+", line[3])))
                worker_mem_percentage.append("".join(re.findall(r"[0-9.]+", line[4])))
        return worker_cpu_core, worker_cpu_percentage, worker_mem_amount, worker_mem_percentage
    
    # given edge cluster nodes are probably closer to each other, the load-balance deployment inside per cluster will be handled by the master node itself
    def find_metric_average():
        worker_cpu_core, worker_cpu_percentage, worker_mem_amount, worker_mem_percentage = Resource_matric_fetcher.filter_metric_result()
        cpu_core_average = sum([float(x) for x in worker_cpu_core]) / len(worker_cpu_core)
        cpu_percentage_average = sum([float(x) for x in worker_cpu_percentage]) / len(worker_cpu_percentage)
        mem_amount_average = sum([float(x) for x in worker_mem_amount]) / len(worker_mem_amount)
        mem_percentage_average = sum([float(x) for x in worker_mem_percentage]) / len(worker_mem_percentage)
        return cpu_core_average, cpu_percentage_average, mem_amount_average, mem_percentage_average

class Network_metric_fetcher:

    iperf_destination = os.environ.get('IPERF_DEST_PORT')

    def fetch_ping_result(neighbor_url):
        ping_command = ["ping", "-c", "5", neighbor_url]
        return subprocess.run(ping_command, capture_output=True, text=True)

    def fetch_iperf_result(neighbor_url):
        iperf_command = ["iperf", "-c", neighbor_url, "-p", Network_metric_fetcher.iperf_destination, "-t", "5"]
        return subprocess.run(iperf_command, capture_output=True, text=True)
    
    def filter_network_metric(neighbor_url):
        ping_result_raw = Network_metric_fetcher.fetch_ping_result(neighbor_url)
        print(ping_result_raw)
        
        iperf_result_raw = Network_metric_fetcher.fetch_iperf_result(neighbor_url)
        print(iperf_result_raw)
        
        # filter average rtt -> in ms
        print("raw = ", ping_result_raw)
        print("stdout = ", ping_result_raw.stdout)
        print("s1 = ", ping_result_raw.strip().split('\n')[-1])
        print("s2 = ", iperf_result_raw.strip().split('\n')[-1].split('=')[1])
        print("s3 = ", iperf_result_raw.strip().split('\n')[-1].split('=')[1].strip().split('/')[1])
        ping_result = ping_result_raw.strip().split('\n')[-1].split('=')[1].strip().split('/')[1]
        print(iperf_result_raw.split('\n')[-1].split('=')[1].strip())
        
        # filter average bandwidth -> in Gbit/s
        iperf_result = iperf_result_raw.strip().split('\n')[-1].split()[-2] 
        print(iperf_result_raw.split('\n')[-1])
        
        return ping_result, iperf_result

class Write_metrics_to_file():
    def construct_network_log(cluster_id):
        while True:
            # bugfix: mappinig b/t name, id, ip
            cluster_ip = os.environ.get('CLUSTER_IP')
            ping_result, iperf_result = Network_metric_fetcher.filter_network_metric(cluster_ip)

            rows = []

            # Try reading the existing content and update
            try:
                with open(networklog, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row[0] == cluster_id:
                            rows.append([cluster_id, ping_result, iperf_result])
                            found = True
                        else:
                            rows.append(row)
            except FileNotFoundError:
                pass

            # Sort rows by cluster_id
            rows.sort(key=lambda x: int(x[0].split('_')[-1]))

            # Write the updated content back
            with open(networklog, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            time.sleep(network_interval)

    def construct_metric_log(cluster_id, cpu_core_average, cpu_percentage_average, mem_amount_average, mem_percentage_average):
        rows = []
        
        # Try reading the existing content and update
        try:
            with open(metriclog, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == cluster_id:
                        rows.append([cluster_id, cpu_core_average, cpu_percentage_average, mem_amount_average, mem_percentage_average])
                        found = True
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

class Send_packet():
    def send_data(cluster_name, local_url, max_hop):
        cpu_usage, cpu_percentage, ram_usage, ram_percentage = Resource_matric_fetcher.find_metric_average()
        while True:
            current_hop = max_hop
            all_neighbors = get_neighbor_urls()
            for ip in all_neighbors:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((ip, peer_update_port))
                        data_packet = f"Type: 1, Current_Hop: {current_hop}, Max_Hop: {max_hop}, Sender_ID: {local_url}, Receiver_ID: {ip}, CPU_amount: {cpu_usage},CPU_percentage: {cpu_percentage}, RAM_usage: {ram_usage}, RAM_percentage: {ram_percentage}"
                        client_socket.send(data_packet.encode())
                        print(f"Sent data to {ip}", flush=True)

                        Write_metrics_to_file.construct_metric_log(cluster_name, cpu_usage, cpu_percentage, ram_usage, ram_percentage)
                    
                except ConnectionRefusedError:
                    print(f"Failed to connect to {ip}", flush=True)
        
            time.sleep(peer_update_interval)

if __name__ == "__main__":
    
    print(f'\n{peer_update_port=}\n')
    
    update_network_thread = threading.Thread(target=Write_metrics_to_file.construct_network_log, args=(cluster_name, ))
    
    send_data_thread = threading.Thread(target=Send_packet.send_data, args=(cluster_name, local_url, max_hop))
    
    update_network_thread.start()
    send_data_thread.start()
    
    while True:
        time.sleep(1)