from fastapi import FastAPI, UploadFile, HTTPException
import os
import subprocess

app = FastAPI()

deployment_dir = os.environ.get('DEPLOYMENT_DIR')
deploymentlog = os.environ.get('DEPLOYMENT_LOG')

'''
TODO:
    1. from metric log, update decision
    2. receive yaml files from endpoint
    3. apply yaml file to cluster
'''

@app.post("/deployment")
async def read_root(file: UploadFile = None):
    if file:
        content_type = file.content_type  # Check the content type of the uploaded file
        if content_type == "application/yaml":
            try:
                file_path = os.path.join(deployment_dir, file.filename)
                with open(file_path, 'wb+') as buffer:
                    content = file.file.read()  # Read the content directly
                    buffer.write(content)
                # Run the bash command
                cmd = ["kubectl", "apply", "-f", file_path]
                with open(deploymentlog, 'a') as log_file:  # Open the log file in append mode
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
                    log_file.write(result.stdout)
                return result
            except Exception as e:
                return {"message": f"Error handling file: {str(e)}"}
        else:
            return {"message": "File not uploaded or not a valid application/yaml file."}
    else:
        return {"message": "No file uploaded."}
    
