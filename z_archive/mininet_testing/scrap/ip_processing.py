import argparse
import subprocess

default_exec_path = "/home/jack/Desktop/mininet/RAFT-like/raft_test.py"

def process_ips(node_ip, neighbor_ips, port_number):
    # Process the array of IP tuples here
    processed_ips_tuple = []
    node_ip_tuple = ("node_ip", "port_number")
    for ip in neighbor_ips:
        processed_ips_tuple.append(("ip", "port_number"))
    
    return node_ip_tuple, processed_ips_tuple

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process neighbor IP addresses into tuples.')
    parser.add_argument('node_name', help='Name of this node (e.g., h1)')
    parser.add_argument('node_ip', help='IP address of this node')
    parser.add_argument('neighbor_ips', nargs='+', help='Neighbor IP addresses')
    parser.add_argument('port_number', type=int, help='Port number of nodes')
    args = parser.parse_args()

    node_ip_tuple, processed_ips_tuple = process_ips(args.node_ip, args.neighbor_ips, args.port_number)

    # print out the processed IPs
    print("\n\nHello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
    print(args.node_name, args.node_ip, args.neighbor_ips, "\n\n")
    print(node_ip_tuple, processed_ips_tuple, "\n\n")
    for ip in processed_ips_tuple:
        print(ip)

    # Call the main script with the processed arguments
    cmd = ["sudo", "python3", default_exec_path, args.node_name, node_ip_tuple, processed_ips_tuple]
    subprocess.run(cmd)
