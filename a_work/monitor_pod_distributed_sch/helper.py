import os
import json
import csv

class File_management:
    def append_to_file(abs_path, file_name, data):
        with open(os.path.join(abs_path, file_name), 'a') as f:
            f.write(data)
            
    def write_to_file(abs_path, file_name, data):
        with open(os.path.join(abs_path, file_name), 'w') as f:
            f.write(data)
    
    def read_from_file(abs_path, file_name):
        with open(os.path.join(abs_path, file_name, 'r')) as f:
            return f.read()
    
    def check_file_exist(abs_path, file_name):
        if os.path.exists(os.path.join(abs_path, file_name)):
            return True
        else:
            return False

class Update_own_csv:
    
    def fetch_cluster_name():
        return os.environ.get('NODE_NAME')
    
    def update_own_network(data_type, data):
        cluster_name = Update_own_csv.fetch_cluster_name()
        network_metric_file_path = os.environ.get('NETWORK_LOG')
        file_exists = os.path.isfile(network_metric_file_path)
        existing_data = {}

        if file_exists:
            with open(network_metric_file_path, mode='r') as csv_file:
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

        with open(network_metric_file_path, mode='w', newline='') as csv_file:
            fieldnames = ['node', 'latency', 'bandwidth']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for cluster, values in existing_data.items():
                writer.writerow({'node': cluster, 'latency': values['latency'], 'bandwidth': values['bandwidth']})
    
    def update_own_metric(data_type, data):
        cluster_name = Update_own_csv.fetch_cluster_name()
        resource_metric_file_path = os.environ.get('METRIC_LOG')
        file_exists = os.path.isfile(resource_metric_file_path)
        existing_data = {}
        
        if file_exists:
            with open(resource_metric_file_path, mode='r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    existing_data[row['node']] = {
                        'cpu_core': row['cpu_core'],
                        'cpu_percentage': row['cpu_percentage'],
                        'mem_amount': row['mem_amount'],
                        'mem_percentage': row['mem_percentage']
                    }

        if data_type == 'cpu_core':
            existing_data[cluster_name]['cpu_core'] = data
        elif data_type == 'cpu_percentage':
            existing_data[cluster_name]['cpu_percentage'] = data
        elif data_type == 'mem_amount':
            existing_data[cluster_name]['mem_amount'] = data
        elif data_type == 'mem_percentage':
            existing_data[cluster_name]['mem_percentage'] = data
        else:
            print("Invalid data_type. Supported values are 'latency' and 'bandwidth'.")

        with open(resource_metric_file_path, mode='w', newline='') as csv_file:
            fieldnames = ['node', 'latency', 'bandwidth']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for cluster, values in existing_data.items():
                writer.writerow({'node': cluster, 'latency': values['latency'], 'bandwidth': values['bandwidth']})
    

