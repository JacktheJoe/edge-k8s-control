import argparse
import os
import time
from pysyncobj import SyncObj, replicated

interval = 10
file_path = "/home/jack/Desktop/mininet/RAFT-like/results/results_node/"

class MySyncObj(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs, nodeName):
        super(MySyncObj, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.leader_decision = None
        self.node_name = nodeName

    @replicated
    def update_leader_decision(self, decision):
        self.leader_decision = decision

def parse_arguments():
    parser = argparse.ArgumentParser(description='Sync leader decision on lowest util node.')
    parser.add_argument('node_name', help='Name of this node (e.g., node1)')
    parser.add_argument('node_ip', help='IP address of this node (e.g., localhost:4321)')
    parser.add_argument('neighbor_ips', nargs='+', help='IP addresses of neighbor nodes (e.g., localhost:4322 localhost:4323)')
    return parser.parse_args()

def get_lowest_node(node_name):
    txt_file = os.path.join(file_path, f"{node_name}.txt")
    with open(txt_file, mode='r', newline='') as file:
        lowest_node_name = file.readline()
    return lowest_node_name

def offload_decision(node_name):
    lowest_node_name = get_lowest_node(node_name)
    lowest_node_ip = f"10.0.0.{lowest_node_ip[1]}"
    decision = (lowest_node_name, lowest_node_ip)
    syncObj.update_leader_decision(decision)

if __name__ == "__main__":
    args = parse_arguments()

    # Create synchronized object with parsed addresses
    syncObj = MySyncObj(args.node_name, args.node_ip, args.neighbor_ips)

    while True:
        time.sleep(interval)
        offload_decision(args.node_name)
    # Implement the logic for determining the lowest utilization node
    # and updating the leader decision.
    # Example:
    # if is_this_node(lowest_util_node):
    #     decision = (args.node_name, '10.0.0.1')  # example decision
    #     syncObj.update_leader_decision(decision)
