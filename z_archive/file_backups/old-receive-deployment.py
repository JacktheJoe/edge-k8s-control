from fastapi import FastAPI, UploadFile, HTTPException
import os
import subprocess
import httpx
import json
import glob

app = FastAPI()

BASE_UPLOAD_DIRECTORY = "/code/outputs"

# Define the cluster URLs
all_clusters = {
    "cluster_1": "http://10.200.31.10:30002/optimized",
    "cluster_2": "http://10.200.32.10:30002/optimized",
    "cluster_3": "http://10.200.33.10:30002/optimized"
}

# Ensure base directory exists
if not os.path.exists(BASE_UPLOAD_DIRECTORY):
    os.makedirs(BASE_UPLOAD_DIRECTORY)

def save_and_apply_yaml(file: UploadFile, subdirectory: str):
    directory = os.path.join(BASE_UPLOAD_DIRECTORY, subdirectory)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the path where the file will be saved
    file_path = os.path.join(directory, file.filename)

    # Save the uploaded file to the defined path
    with open(file_path, 'wb+') as buffer:
        content = file.read()
        buffer.write(content)

    # Run the bash command
    cmd = ["kubectl", "apply", "-f", file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode != 0:
        raise Exception(result.stderr)

    return {"filename": file.filename, "message": result.stdout.strip()}

def average_percent_ram_value_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        
    # Assuming the JSON file has a "general" section with "percent_RAM" values
    percent_ram_value = float(data["data"]["general"]["percent_RAM"])
    return percent_ram_value

def average_percent_cpu_value_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
        
    # Assuming the JSON file has a "general" section with "percent_CPU" values
    percent_cpu_value = float(data["data"]["general"]["percent_CPU"])
    return percent_cpu_value

def get_latest_json_file(directory):
    json_files = glob.glob(f"{directory}/*.json")
    
    if not json_files:
        raise Exception(f"No JSON files found in {directory}.")
    
    latest_file = max(json_files, key=lambda x: os.path.getctime(x))
    return latest_file

def get_current_cluster_name():
    # Fetch the subnet information from the environment variable (assuming the environment variable setup remains the same)
    subnet = os.environ.get('SUBNET_ID', '')
    ip = subnet.split('/')[0]
    octets = ip.split('.')
    if len(octets) >= 3:
        third_octet = octets[2]
        if len(third_octet) >= 2:
            second_digit = third_octet[1]
            current_cluster_name = f"cluster_{second_digit}"
            return current_cluster_name
    return None

def get_cluster_url(cluster_name, cluster_mapping):
    if cluster_name in cluster_mapping:
        return cluster_mapping[cluster_name]
    else:
        return None

def compare():
    # Check the current cluster and adjust its directory path
    CURRENT_CLUSTER = get_current_cluster_name()
    
    # Define cluster directories
    cluster_dirs = {
        cluster_name: os.path.join(BASE_UPLOAD_DIRECTORY, cluster_name)
        for cluster_name in ["cluster_1", "cluster_2", "cluster_3"]
    }

    # Update the cluster directory if the current cluster matches
    if CURRENT_CLUSTER in cluster_dirs:
        cluster_dirs["local_machine"] = os.path.join(BASE_UPLOAD_DIRECTORY, "local_machine")
        del cluster_dirs[CURRENT_CLUSTER]

    # Calculate resource utilizations for the current cluster ("local_machine") and the remaining clusters
    utilizations = {}
    for cluster, directory in cluster_dirs.items():
        try:
            latest_json = get_latest_json_file(directory)
            utilizations[cluster] = {
                "ram": average_percent_ram_value_from_json(latest_json),
                "cpu": average_percent_cpu_value_from_json(latest_json)
            }
        except Exception as e:
            # Handle the exception and provide a more informative error message
            return f"Error: {str(e)}"

    # Determine the cluster with the lowest resource utilization
    if utilizations:
        lowest_utilization_cluster = min(utilizations, key=lambda cluster: (utilizations[cluster]["ram"], utilizations[cluster]["cpu"]))
        return all_clusters[lowest_utilization_cluster]
    else:
        return "No JSON files found in any cluster directory."


@app.get("/")
async def read_root(file: UploadFile = None):
    if file and file.filename.endswith('.yaml'):
        # Read the content of the uploaded file
        file_content = await file.read()

        # Return the content of the uploaded file as is
        return file_content

    return {"message": "File not uploaded or not a valid .yaml file."}

@app.post("/direct/")
async def direct_upload(file: UploadFile = None):
    if file and file.filename.endswith('.yaml'):
        content = await file.read()
        
        lowest_utilization_cluster_name = compare()
        
        if lowest_utilization_cluster_name != "local_machine":
            lowest_utilization_cluster_url = get_cluster_url(lowest_utilization_cluster_name, all_clusters)
            
            if lowest_utilization_cluster_url:
                # Send the content to the cluster with the lowest resource utilization
                async with httpx.AsyncClient() as client:
                    response = await client.post(lowest_utilization_cluster_url, data=content, headers={"Content-Type": "application/yaml"})
                    if response.status_code != 200:
                        raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
            return {"message": f"YAML content sent to cluster with lower resource utilization: {lowest_utilization_cluster_name} ."}
        else:
            # Save the YAML file with save_and_apply_yaml
            result = save_and_apply_yaml(file, "local_machine")
            return {"message": f"YAML content not sent as lowest_utilization_cluster_name is 'local_machine'. \nResult is: {result}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")

@app.get("/optimized")
async def read_root(file: UploadFile = None):
    if file and file.filename.endswith('.yaml'):
        # Read the content of the uploaded file
        content = await file.read()
        result = save_and_apply_yaml(file, "local_machine")
        return {"message": "File from other clusters been applied on local node."}
    else:
        return {"message": "File not uploaded or not a valid .yaml file."}