# app.py,  to test checkpointing pause time on data server
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')
    client_ip = request.remote_addr
    timestamped_data = f"{datetime.now()}: {client_ip}: {data}\n"
    with open("received_data.txt", "a") as file:
        file.write(timestamped_data)
    return "Data received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23333)
