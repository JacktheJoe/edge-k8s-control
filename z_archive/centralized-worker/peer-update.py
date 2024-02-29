from fastapi import FastAPI, Request
import datetime
import os
import subprocess
import json

output_path_basic = "/code/outputs/"

# Ensure directory exists
if not os.path.exists(BASE_UPLOAD_DIRECTORY):
    os.makedirs(BASE_UPLOAD_DIRECTORY)

if not os.path.exists(yaml_directory):
    os.makedirs(yaml_directory)

if not os.path.exists(redirected_directory):
    os.makedirs(redirected_directory)

# for example, all under /24 network
# sent from 10.200.32.10 ==> from 32 ==> cluster_2
def cluster_id(id):
    last_digit = id % 10
    return f"cluster_{last_digit}"

# create dir if not exist
def check_output_dir(cluster_name):
    save_path = output_path_basic + cluster_name
    isExist = os.path.exists(save_path)
    if not isExist:
        os.makedirs(save_path)
        print(save_path)
    return

app = FastAPI()

@app.post("/")
async def get_body(request: Request):
    # format received data
    received = await request.json()
    data = json.dumps(received, indent=2)

    # handle save location on log server
    sent_from = received[list(received.keys())[0]].split('.')[-2]
    cluster_name = cluster_id(int(sent_from))
    check_output_dir(cluster_name)

    # save file to location
    file_indicator = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
    filename = output_path_basic + cluster_name + "/" + file_indicator
    print(filename)
    with open(filename+'.json', 'w+') as resFile:
        resFile.write(data)
        resFile.close()
    return{"data": data}