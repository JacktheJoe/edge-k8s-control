from fastapi import FastAPI, UploadFile, HTTPException
import os
import subprocess
import time

import average

app = FastAPI()

BASE_UPLOAD_DIRECTORY = "/code/outputs"
yaml_directory = "/code/deployment"
redirected_directory = "/code/redirected"

# Define the cluster URLs
all_clusters = {
    "cluster_1": "http://10.200.31.10:30002/optimized",
    "cluster_2": "http://10.200.32.10:30002/optimized",
    "cluster_3": "http://10.200.33.10:30002/optimized"
}

def get_current_cluster_name():
    # Fetch the subnet information from the environment variable (assuming the environment variable setup remains the same)
    subnet = os.environ.get('NODE_IP', '')
    ip = subnet.split('/')[0]
    octets = ip.split('.')
    if len(octets) >= 3:
        third_octet = octets[2]
        if len(third_octet) >= 2:
            second_digit = third_octet[1]
            current_cluster_name = f"cluster_{second_digit}"
            return current_cluster_name

# save to yaml_directory for direct-deployments
def save_and_apply_yaml(file: UploadFile):
    cluster_name = get_current_cluster_name()
    if cluster_name:
        directory = os.path.join(yaml_directory, cluster_name)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Define the path where the file will be saved
        file_path = os.path.join(directory, file.filename)

        try:
            # Save the uploaded file to the defined path
            with open(file_path, 'wb+') as buffer:
                content = file.file.read()  # Read the content directly
                buffer.write(content)

            # Run the bash command
            cmd = ["kubectl", "apply", "-f", file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Check if the command was successful
            if result.returncode == 0:
                return {"filename": file.filename, "message": result.stdout.strip()}
            else:
                raise Exception(result.stderr)
        except Exception as e:
            # Print the exception message for debugging
            print(f"Error saving and applying YAML file: {str(e)}")
            raise Exception(f"Error saving and applying YAML file: {str(e)}")
    else:
        return {"message": f"Cluster name is not available. Received: {cluster_name}"}

def send_out(file_path, url):
    curl_command = [
    "curl",
    "-X", "POST",
    "-F", f"file=@{file_path};type=application/yaml",
    url
    ]

    result = subprocess.run(curl_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("Curl command executed successfully.")
        print("Response:", result.stdout)
    else:
        print("Error executing curl command:")
        print("Error message:", result.stderr)

@app.post("/direct")
async def direct_upload(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            content = await file.read()
            lowest_utilization_cluster_url = average.compare()

            file_path = os.path.join(redirected_directory, file.filename)
            with open(file_path, 'wb+') as buffer:
                content = file.file.read()  # Read the content directly
                buffer.write(content)

            time.sleep(0.5)

            send_out(file_path, lowest_utilization_cluster_url)  # Await the asynchronous function

            return {"message": f"YAML content sent to cluster with lower resource utilization: {lowest_utilization_cluster_url}"}
        else:
            # Save the YAML file with save_and_apply_yaml
            result = save_and_apply_yaml(file, "local_machine")
            return {"message": f"YAML content not sent as lowest_utilization_cluster_name is 'local_machine'. \nResult is: {result}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")

@app.post("/optimized")
async def read_root(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            try:
                file_path = os.path.join(yaml_directory, file.filename)
                with open(file_path, 'wb+') as buffer:
                    content = file.file.read()  # Read the content directly
                    buffer.write(content)
                # Run the bash command
                cmd = ["kubectl", "apply", "-f", file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(cmd, result)
                return result
            except Exception as e:
                return {"message": f"Error handling file: {str(e)}"}
        else:
            return {"message": "File not uploaded or not a valid application/yaml file."}
    else:
        return {"message": "No file uploaded."}