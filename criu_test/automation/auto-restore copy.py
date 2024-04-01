from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/var/lib/kubelet/checkpoints'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/build', methods=['POST'])
def build_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file:
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
