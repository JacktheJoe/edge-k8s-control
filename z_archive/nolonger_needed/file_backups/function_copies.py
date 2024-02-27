@app.post("/optimized")
async def read_root(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            file_path = os.path.join(yaml_directory, file.filename)
            with open(file_path, 'wb+') as buffer:
                content = file.file.read()  # Read the content directly
                buffer.write(content)
            cmd = ["kubectl", "apply", "-f", file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Check if the command was successful
            if result.returncode == 0:
                return {"filename": file.filename, "message": result.stdout.strip()}
            else:
                raise Exception(result.stderr)
        else:
            return {"message": "File not uploaded or not a valid application/yaml file."}
    else:
        return {"message": "No file uploaded."}


@app.post("/optimized")
async def read_root(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            try:
                result = save_and_apply_yaml(file)
                return result
            except Exception as e:
                return {"message": f"Error saving and applying YAML file: {str(e)}"}
        else:
            return {"message": "File not uploaded or not a valid application/yaml file."}
    else:
        return {"message": "No file uploaded."}


@app.post("/direct")
async def direct_upload(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            lowest_utilization_cluster_url = compare()  # Get the name of the cluster
            file_path = os.path.join(redirected_directory, file.filename)
            with open(file_path, 'wb+') as buffer:
                content = file.file.read()  # Read the content directly
                buffer.write(content)
            with open(file_path, "rb") as yaml_file:
                yaml_content = yaml_file.read()
            async with httpx.AsyncClient() as client:
                response = await client.post(lowest_utilization_cluster_url, data=yaml_content, headers={"Content-Type": "application/yaml"})
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
                return {"message": f"YAML content sent to cluster with url: {lowest_utilization_cluster_url}, response is: {response}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")
    else:
        raise HTTPException(status_code=400, detail="No file uploaded.")


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
    
    
    
@app.post("/direct")
async def direct_upload(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            lowest_utilization_cluster_url = compare()  # Get the name of the cluster
            file_path = os.path.join(redirected_directory, file.filename)
            with open(file_path, 'wb+') as buffer:
                content = file.file.read()  # Read the content directly
                buffer.write(content)
            with open(file_path, "rb") as yaml_file:
                yaml_content = yaml_file.read()

            response = await send_post_request(lowest_utilization_cluster_url, yaml_content)

            return {"message": f"YAML content sent to cluster with url: {lowest_utilization_cluster_url}, response is: {response}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")
    else:
        raise HTTPException(status_code=400, detail="No file uploaded.")

curl_command = [
    "curl",
    "-X", "POST",
    "-F", "file=@/home/jack/nginx.yaml;type=application/yaml",
    "http://10.200.31.10:30002/direct"
]

try:
    result = subprocess.run(curl_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print("Curl command executed successfully.")
        print("Response:", result.stdout)
    else:
        print("Error executing curl command:")
        print("Error message:", result.stderr)
except subprocess.CalledProcessError as e:
    print("Error executing curl command (non-zero exit code):")
    print("Error message:", e.stderr)

async def send_out(file_path, url):
    try:
        with open(file_path, "rb") as yaml_file:
            yaml_content = yaml_file.read()
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=yaml_content, headers={"Content-Type": "application/yaml"})
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
        return "sent"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending YAML file: {str(e)}")

async def send_post_request(lowest_utilization_cluster_url, yaml_content):
    async with httpx.AsyncClient() as client:
        response = await client.post(lowest_utilization_cluster_url, data=yaml_content, headers={"Content-Type": "application/yaml"})
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
        return response



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