from fastapi import FastAPI, Request
import uvicorn
import json

port_choice=8080

app = FastAPI()

# for example, all under /24 network
# sent from 10.200.32.10 ==> from 32 ==> cluster_2
def cluster_id(id):
    last_digit = id % 10
    return f"cluster_{last_digit}"

# deployment
@app.post("/")
async def get_body(request: Request):
    # format received data
    received = await request.json()
    data = json.dumps(received, indent=2)

    # handle save location on log server
    sent_from = cluster_id(int(received[list(received.keys())[0]].split('.')[-2]))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port_choice)