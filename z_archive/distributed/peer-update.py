from fastapi import FastAPI, Request
import datetime
import os
import subprocess
import json
import time
import csv

all_clusters = {
    "cluster1": "10.200.31.10",
    "cluster2": "10.200.32.10",
    "cluster3": "10.200.33.10"
}
output_path_basic = "/code/outputs/"
network_log = "/code/network_logs.csv"
iperf_port = os.environ['IPERF_SERVER_PORT']
iperf_interval = 60
ping_interval = 30

# for example, all under /24 network
# sent from 10.200.32.10 ==> from 32 ==> cluster_2
def cluster_id(id):
    last_digit = id % 10
    return f"cluster_{last_digit}"

# create dir if not exist
def check_output_dir(cluster_name):
    save_path = output_path_basic + cluster_name
    isExist = os.path.exists(save_path)
    if not isExist:
        os.makedirs(save_path)
        print(save_path)
    return

def write_to_file(file_path, cluster_name, data_type, data):
    file_exists = os.path.isfile(file_path)
    existing_data = {}

    if file_exists:
        with open(file_path, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                existing_data[row['node']] = {
                    'latency': row['latency'],
                    'bandwidth': row['bandwidth']
                }

    if data_type == 'latency':
        existing_data[cluster_name]['latency'] = data
    elif data_type == 'bandwidth':
        existing_data[cluster_name]['bandwidth'] = data
    else:
        print("Invalid data_type. Supported values are 'latency' and 'bandwidth'.")

    with open(file_path, mode='w', newline='') as csv_file:
        fieldnames = ['node', 'latency', 'bandwidth']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for cluster, values in existing_data.items():
            writer.writerow({'node': cluster, 'latency': values['latency'], 'bandwidth': values['bandwidth']})

def check_iperf(ip):
    try:
        iperf_cmd = ["iperf", "-c", ip, "-p", iperf_port, "-t", str(iperf_interval)]
        raw_result = subprocess.run(iperf_cmd, capture_output=True, text=True).stdout
        last_line_section = raw_result.strip().split('\n')[-1].split()
        bandwidth = last_line_section[-2] if len(last_line_section) >= 2 else "No value found"
        return bandwidth
    except subprocess.CalledProcessError as e:
        return None, str(e)

def check_ping(ip):
    try:
        ping_cmd = ["ping", "-c", "5", ip]
        raw_result = subprocess.run(ping_cmd, capture_output=True, text=True).stdout
        last_line_section = raw_result.strip().split('\n')[-1].split(' ')[-2].split('/')
        latency = last_line_section[1] if len(last_line_section) >= 2 else "No value found"
        return latency
    except subprocess.CalledProcessError as e:
        return None, str(e)

def network_check():
    # while time interval is not reached, call check ping and check iperf
    while True:
        time.sleep(ping_interval)
        for cluster, ip in all_clusters.items():
            ping_check = check_ping(ip)
            iperf_check = check_iperf(ip)
            if ping_check[0] and iperf_check[0]:
                write_to_file(network_log, cluster, 'latency', ping_check[0])
                write_to_file(network_log, cluster, 'bandwidth', iperf_check[0])
            else:
                print ("Error: ", ping_check[1], iperf_check[1])

app = FastAPI()

@app.post("/")
async def get_body(request: Request):
    # format received data
    received = await request.json()
    data = json.dumps(received, indent=2)

    # handle save location on log server
    sent_from = received[list(received.keys())[0]].split('.')[-2]
    cluster_name = cluster_id(int(sent_from))
    check_output_dir(cluster_name)

    # save file to location
    file_indicator = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    filename = output_path_basic + cluster_name + "/" + file_indicator
    print(filename)
    with open(filename+'.json', 'w+') as resFile:
        resFile.write(data)
        resFile.close()
    return{"data": data}

network_check()