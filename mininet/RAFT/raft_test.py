import argparse
import os
import sys
import time
from pysyncobj import SyncObj, replicated
from datetime import datetime

interval = 10
file_path = "/home/jack/Desktop/mininet/RAFT-like/results_node/"
log_path = "/home/jack/Desktop/mininet/RAFT-like/logs/"
decision_path = "/home/jack/Desktop/mininet/RAFT-like/decisions/"
all_ips = ["10.0.0.{}:8080".format(i) for i in range(1, 10)]

is_leader = False

class MySyncObj(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs, nodeName):
        super(MySyncObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.leader_decision = None
        self.node_name = nodeName

    @replicated
    def update_leader_decision(self, decision):
        self.leader_decision = decision

    def get_leader_decision(self):
        return self.leader_decision

def parse_arguments():
    parser = argparse.ArgumentParser(description='Sync leader decision on lowest util node.')
    parser.add_argument('node_name', help='Name of this node')
    parser.add_argument('node_ip', help='IP address of this node')
    parser.add_argument('neighbor_ips', nargs='+', help='IP addresses of neighbor nodes')
    return parser.parse_args()

def get_lowest_node(node_name):
    txt_file = os.path.join(file_path, f"{node_name}.txt")
    with open(txt_file, mode='r', newline='') as file:
        lowest_node_name = file.readline()
    return lowest_node_name

def offload_decision(node_name):
    lowest_node_name = get_lowest_node(node_name)
    lowest_node_ip = f"10.0.0.{lowest_node_name[1]}"
    # print(lowest_node_name, lowest_node_ip)
    time.sleep(0.01)
    decision = (lowest_node_name, lowest_node_ip)
    syncObj.update_leader_decision(decision)

def filter_out_string(string_to_remove):
    # Use a list comprehension to filter out the specified string
    filtered_list = [string for string in all_ips if string != string_to_remove]
    return filtered_list

def record_status_to_file(syncObj, node_name):
    log_file_path = os.path.join(log_path, f"{node_name}.txt")
    with open(log_file_path, 'a') as logfile:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = str(syncObj.getStatus())
        is_ready = str(syncObj.isReady())
        
        logfile.write(f"\nTime: {current_time}\n")
        logfile.write(f"Status: {status}\n")
        logfile.write(f"isReady: {is_ready}\n")

        self_node = status[2]
        leader_node = status[4]
        if self_node == leader_node:
            print(self_node, leader_node)
            is_leader = True

def print_decision_received(node_name):
    if is_leader == False:
        print("Current node is not the leader\n")
        decision_received = syncObj.get_leader_decision()
        print(f"Decision received: {decision_received}\n")

        decision_file_path = os.path.join(decision_path, f"{node_name}.txt")
        with open(decision_file_path, 'a') as decision_file:
            decision_file.write(f"Decision received: {decision_received}\n")


if __name__ == "__main__":
    
    # args = parse_arguments()

    node_name = sys.argv[1]
    node_ip = sys.argv[2]

    neighbor_ips = filter_out_string(node_ip)
    # print("/n/nfiltered list: ", neighbor_ips, "/n/n")

    # Create synchronized object with parsed addresses
    syncObj = MySyncObj(node_ip, neighbor_ips, node_name)

    #3 print_decision_received(node_name)

    # print out the status and election process over time in detail
    for i in range(10):
        record_status_to_file(syncObj, node_name)
        time.sleep(0.1)

    # print_decision_received(node_name)

    # perform decision offload
    while True:
        record_status_to_file(syncObj, node_name)
        time.sleep(interval)
        offload_decision(node_name)
        print_decision_received(node_name)

