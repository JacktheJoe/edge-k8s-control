from flask import Flask, request, jsonify
import subprocess
import traceback
import requests
import os

dirty_ram_threshold = 100

app = Flask(__name__)

# receives migration request from client or cluster master
@app.route('/migration-request', methods=['POST'])
def migration_request():
    if not request.json or 'migration_name' not in request.json or 'target_node_name' not in request.json:
        return "Invalid request", 400
    
    isLocal = "Local"
    
    migration_name = request.json['migration_name']
    target_node_name = request.json['target_node_name']
    check_automation_path = "/home/jack/checkpoint.sh"
    
    # check if target node is part of local cluster, given if input master node's node name
    cluster_id = target_node_name.split('-')[-1]
    if cluster_id != os.environ.get("CLUSTER_ID"):
        isLocal = target_node_name
    
    print("target node is: " + isLocal)

    try:
        output = subprocess.check_output([check_automation_path, migration_name], shell=False).decode()
        source_node, checkpoint_file_name = output.strip().split()
        dirty_ram_size = int(subprocess.run("kubectl top pod -A | grep " + migration_name, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.split()[-1][:-2])

        if dirty_ram_size <= dirty_ram_threshold: 
            checkpoint_request_url = f"http://{source_node}:30006/small-image"
        else:
            checkpoint_request_url = f"http://{source_node}:30006/large-image"
        
        if isLocal == "Local":
            checkpoint_request_url = f"http://{isLocal}:30006/local-build-push"
            
        response = requests.post(checkpoint_request_url, json={"deployment_name": checkpoint_file_name, "isLocal": isLocal})

        if response.status_code == 200:
            return f"Checkpoint file successfully forwarded. Response: {response.text}", 200
        else:
            return f"Failed to forward checkpoint file. Response: {response.text}", 500
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(f"An error occurred: {traceback_str}")
        return f"An error occurred: {str(e)}", 500

# when reverse checkpoint deployment from other cluster, forward to local worker to build / run
def forward_file(file, target_url, deployment_name, size):
    files = {'checkpoint': (f"{deployment_name}.tar", file, 'application/x-tar')}
    data = {'size': size, 'deployment_name': deployment_name}
    response = requests.post(target_url, files=files, data=data)
    return response.text

@app.route('/receive-and-forward-to-worker', methods=['POST'])
def receive_and_forward_to_worker():
    # Check if the request has the file and the additional data
    if 'checkpoint' not in request.files or 'size' not in request.form or 'deployment_name' not in request.form:
        return jsonify(message="Missing data"), 400

    file = request.files['checkpoint']
    size = request.form['size']
    deployment_name = request.form['deployment_name']

    worker_status = subprocess.run("kubectl top nodes | grep worker", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

    forward_raw = next(parts[0] for parts in [line.split() for line in worker_status.strip().split('\n')] if float(parts[-1].rstrip('%')) == min(float(line.split()[-1].rstrip('%')) for line in worker_status.strip().split('\n')))

    forward_target = f"http://{forward_raw}:30006/worker-receive"

    # Forward the file and data immediately
    forward_response = forward_file(file, forward_target, deployment_name, size)

    return jsonify(message="File forwarded successfully", forward_response=forward_response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30005)