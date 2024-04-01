from flask import Flask, request, jsonify
import subprocess
import traceback
import requests

app = Flask(__name__)

yaml_template = """
apiVersion: v1
kind: Pod
metadata:
  name: {deployment_name}
  labels:
    app: {deployment_name}
spec:
  containers:
  - name: {deployment_name}
    image: {image_name}
  nodeName: {target_node_name}
"""

def generate_yaml(deployment_name, image_name, target_node_name):
    return yaml_template.format(
        deployment_name=deployment_name,
        image_name=image_name,
        target_node_name=target_node_name
    )

def run_restore_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def restore_pod(deployment_name, image_name, target_node_name):
    yaml_content = generate_yaml(deployment_name, image_name, target_node_name)
    with open("output.yaml", "w") as f:
        f.write(yaml_content)

    print("yaml content variables: ", deployment_name, image_name, target_node_name)
    
    restore_command = "kubectl apply -f output.yaml"
    run_restore_command(restore_command)

# receives image_name to deploy on node
@app.route('/generate-yaml-restore', methods=['POST'])
def restore_on_local():
    if not request.json or 'deployment_name' not in request.json or 'image_name' not in request.json:
        return jsonify({"error": "Invalid request: missing deployment_name"}), 400

    # deployment_name = request.json['deployment_name']
    deployment_name = "heartbeat-sender-restore"
    image_name = request.json['image_name']
    
    print("Pod about to be restored: ", deployment_name, image_name)
    
    # hardcode target node name for testing
    restore_pod(deployment_name, image_name, "worker-5-1")
    
    return jsonify({"message": "Pod restoration initiated"}), 200

@app.route('/migration-request', methods=['POST'])
def migration_request():
    # Check if both required fields are present in the request
    if not request.json or 'migration_name' not in request.json or 'target_node_name' not in request.json:
        return jsonify({"error": "Invalid request: 'migration_name' and 'target_node' are required."}), 400
    
    migration_name = request.json['migration_name']
    target_node = request.json['target_node_name']  # Retrieve the target node from the request
    check_automation_path = "/home/jack/checkpoint.sh"

    try:
        output = subprocess.check_output([check_automation_path, migration_name], shell=False).decode()
        source_node = output.strip().split()[0]
        checkpoint_file = output.strip().split()[1]
        print("checkpoint done.", output)

        # for testing purpose, delete current deployment
        delete_command = f"kubectl delete -f heartbeat.yaml"
        deleted_source = subprocess.run(delete_command, shell=True, check=True).stdout
        
        print("Source pod deleted", deleted_source)

        # Use the target_node from the request instead of the source_node for the URL
        url = f"http://{source_node}:30006/build-local-image"
        response = requests.post(url, json={"deployment_name": checkpoint_file})

        if response.status_code == 200:
            return jsonify({"message": f"Checkpoint file successfully forwarded to build-local-image on {target_node}. Response: {response.text}"}), 200
        else:
            return jsonify({"error": f"Failed to forward checkpoint file to build-local-image on {target_node}. Response: {response.text}"}), 500
    except Exception as e:
        traceback_str = traceback.format_exc()
        print(f"An error occurred: {traceback_str}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=30005)
