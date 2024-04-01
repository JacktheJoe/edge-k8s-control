from flask import Flask, request
import subprocess
import os
import requests

app = Flask(__name__)

@app.route('/build-local-image', methods=['POST'])
def build_local_image():
    # Extract the deployment_name from the request's data
    if not request.json or 'deployment_name' not in request.json:
        return "Invalid request: missing deployment_name", 400
    
    deployment_name = request.json['deployment_name']

    # Define the path to the bash script
    script_path = "/var/lib/kubelet/checkpoints/build.sh"

    # Check if the script file exists
    if not os.path.exists(script_path):
        return "Error: build.sh script not found.", 500

    # Run the script with the full file path
    try:
        # this result is result of builing image, which returns the image name
        image_name_raw = subprocess.run([script_path, deployment_name], capture_output=True, text=True)
        print("image name raw is: ", image_name_raw)
        
        if image_name_raw.returncode != 0:
            return f"Error during script execution: {image_name_raw.stderr}", 500

        image_name= image_name_raw.stdout.splitlines()[-2].split()[-1]
        print("image name is: ", image_name)

        # for simple testing, using local host name as target node
        restore_result = requests.post('http://master-5:30005/generate-yaml-restore', json={'image_name': image_name, 'deployment_name': deployment_name})

        print("restore result is: ", restore_result)

        return f"Script executed successfully: {restore_result}", 200
    except Exception as e:
        return f"An error occurred while executing the script: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30006)