
async def direct_upload(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            try:
                lowest_utilization_cluster_name = compare()  # Get the name of the cluster
        
                if lowest_utilization_cluster_name:
                    if lowest_utilization_cluster_name != get_current_cluster_name():
                        lowest_utilization_cluster_url = all_clusters.get(lowest_utilization_cluster_name)
                
                        # Send the content to the cluster with the lowest resource utilization
                        async with httpx.AsyncClient() as client:
                            response = await client.post(lowest_utilization_cluster_url, data=file, headers={"Content-Type": "application/yaml"})
                            if response.status_code != 200:
                                raise HTTPException(status_code=500, detail="Error forwarding YAML file.")
                        return {"message": f"YAML content sent to cluster with lower resource utilization: {lowest_utilization_cluster_name}, with url {lowest_utilization_cluster_url} ."}
                    else:
                        # Save the YAML file with save_and_apply_yaml
                        result = save_and_apply_yaml(file)
                        
                        raise HTTPException(status_code=400, detail=f"YAML content not sent as lowest_utilization_cluster_name is local cluster. \nResult is: {result}")
                else:
                    raise HTTPException(status_code=400, detail="No clusters available for processing the file.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error saving and applying YAML file: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .yaml file.")
    else:
        raise HTTPException(status_code=400, detail="No file uploaded.")