import asyncio
import os
import httpx
from fastapi import HTTPException, UploadFile

# Assuming the rest of your FastAPI setup is in place

async def process_and_send_file(file, lowest_utilization_cluster_url):
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
    
    return f"YAML content sent to cluster with url: {lowest_utilization_cluster_url}, response is: {response}"

@app.post("/direct")
async def direct_upload(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            lowest_utilization_cluster_url = compare()  # Get the name of the cluster

            # Run the file processing and HTTP request asynchronously
            result = await process_and_send_file(file, lowest_utilization_cluster_url)
            
            return {"message": result}
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")
    else:
        raise HTTPException(status_code=400, detail="No file uploaded.")



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
            # stupid async function
            async with httpx.AsyncClient() as client:
                response = await client.post(lowest_utilization_cluster_url, data=yaml_content, headers={"Content-Type": "application/yaml"})
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
                return {"message": f"YAML content sent to cluster with url: {lowest_utilization_cluster_url}, response is: {response}"}
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")
    else:
        raise HTTPException(status_code=400, detail="No file uploaded.")