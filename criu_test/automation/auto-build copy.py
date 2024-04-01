from flask import Flask, request, jsonify
import subprocess
import requests
import os

app = Flask(__name__)

def build():
    # Define the path to the bash script
    script_path = "/var/lib/kubelet/checkpoints/build.sh"

    if not os.path.exists(script_path):
        return "Error: build.sh script not found.", 500

    # Run the script with the full file path
    try:
        result = subprocess.run([script_path, deployment_name], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error during script execution: {result.stderr}", 500
        return f"Script executed successfully: {result.stdout}", 200
    except Exception as e:
        return f"An error occurred while executing the script: {str(e)}", 500

# sends checkpoint to build on target node
def send(isLocal, checkpoint_filename, deployment_name, size):
    if not os.path.exists(checkpoint_filename):
        return "File not found"

    target_url = f"http://{isLocal}:30006/build"

    with open(checkpoint_filename, 'rb') as f:
        files = {'checkpoint': (checkpoint_filename, f)}
        data = {'size': size, 'deployment_name': deployment_name}
        response = requests.post(target_url, files=files, data=data)

    return "File sent successfully, response: " + response.text

# small image gets send to and build on target node
@app.route('/small-image', methods=['POST'])
def build_local_image():
    if not request.json or 'deployment_name' or 'isLocal' not in request.json:
        return "Invalid request: missing deployment_name", 400
    
    deployment_name = request.json['deployment_name']
    isLocal = request.json['isLocal']

    if isLocal == "Local":
        return build(deployment_name, isLocal)
    else:
        return send(deployment_name, isLocal)    

# large image gets checked and if then send to registry
@app.route('/large-image', methods=['POST'])
def build_local_image():
    if not request.json or 'deployment_name' or 'isLocal' not in request.json:
        return "Invalid request: missing deployment_name", 400
    
    deployment_name = request.json['deployment_name']
    isLocal = request.json['isLocal']
    # Define the path to the bash script
    script_path = "/var/lib/kubelet/checkpoints/build.sh"

    if not os.path.exists(script_path):
        return "Error: build.sh script not found.", 500

    # Run the script with the full file path
    try:
        result = subprocess.run([script_path, deployment_name], capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error during script execution: {result.stderr}", 500
        return f"Script executed successfully: {result.stdout}", 200
    except Exception as e:
        return f"An error occurred while executing the script: {str(e)}", 500

# worker receives data from other cluster forwarded by local master
@app.route('/worker-receive', methods=['POST'])
def worker_receive():
    if 'checkpoint' not in request.files or 'size' not in request.form or 'deployment_name' not in request.form:
        return jsonify(message="Missing data"), 400

    file_save_path = "/var/lib/kubelet/checkpoints"

    file = request.files['checkpoint']
    size = request.form['size']
    deployment_name = request.form['deployment_name']
    
    if file:
        # possible to use secure_filename to ensure security of symbol injection?
        filename = file.filename
        file.save(os.path.join(file_save_path, filename))
        return 'Received file saved successfully as {}'.format(filename)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30006)
