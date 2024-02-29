import os
import json
import glob

BASE_UPLOAD_DIRECTORY = "/code/outputs" 

all_clusters = {
    "cluster_1": "http://10.200.31.10:30002/optimized",
    "cluster_2": "http://10.200.32.10:30002/optimized",
    "cluster_3": "http://10.200.33.10:30002/optimized"
}

def average_percent_value_from_json(json_file_path, key):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        
    # Assuming the JSON file has a "general" section with specified key values
    value = float(data.get("data", {}).get("general", {}).get(key, 0))
    return value

def get_latest_json_file(directory):
    json_files = glob.glob(f"{directory}/*.json")
    
    if not json_files:
        raise Exception(f"No JSON files found in {directory}.")
    
    latest_file = max(json_files, key=lambda x: os.path.getctime(x))
    return latest_file

def compare():
    utilizations = {}
    for cluster, url in all_clusters.items():
        try:
            directory = os.path.join(BASE_UPLOAD_DIRECTORY, cluster)
            latest_json = get_latest_json_file(directory)
            utilizations[cluster] = {
                "ram": average_percent_value_from_json(latest_json, "percent_RAM"),
                "cpu": average_percent_value_from_json(latest_json, "percent_CPU")
            }
        except Exception as e:
            # Handle the exception and provide a more informative error message
            return f"Error: {str(e)}"

    # Determine the cluster with the lowest resource utilization
    if utilizations:
        lowest_utilization_cluster = min(utilizations, key=lambda cluster: (utilizations[cluster]["ram"], utilizations[cluster]["cpu"]))
        # return the url to optimize
        return all_clusters.get(lowest_utilization_cluster)
    else:
        return "No JSON files found in any cluster directory."