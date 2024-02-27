import json
from flask import Flask, request

app = Flask(__name__)

Base_URL = '/'

@app.route(Base_URL, methods=['POST'])
def test_post():
    data = request.get_data()
    print(type(data))
    print(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20000)
