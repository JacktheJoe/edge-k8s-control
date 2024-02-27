from fastapi import FastAPI, UploadFile, HTTPException
import os
import subprocess
import time

app = FastAPI()

# Define the cluster URLs
all_clusters = {
    "cluster_1": "http://10.200.31.10:30002/optimized",
    "cluster_2": "http://10.200.32.10:30002/optimized",
    "cluster_3": "http://10.200.33.10:30002/optimized"
}

def send_cluster_id(cluster_id):
    endpoint_url = "http://example.com/your_endpoint"  # Replace with your actual endpoint URL

    # Prepare the curl command
    curl_command = [
        "curl",
        "-X", "POST",
        "-d", f"cluster_id={cluster_id}",
        endpoint_url
    ]

    # Execute the curl command
    try:
        subprocess.run(curl_command, check=True)
        print(f"Successfully sent cluster_id={cluster_id} to {endpoint_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Example usage:
cluster_id_to_send = "cluster_1"
send_cluster_id(cluster_id_to_send)

async def read_consensus(name: str):
    file_path = "/code/decision.txt"
    with open(file_path, mode="w") as file:
        file.write(f"{name}\n")
    
    return {"message": f"Received : {name}"}

@app.post("/")
async def read_consensus_endpoint(name: str):
    return await read_consensus(name)
