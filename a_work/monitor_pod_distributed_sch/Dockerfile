FROM python:3.9

# environment variables for different ports and time intervals
ENV IPERF_SERVER_PORT=5201
ENV METRIC_UPDATE_receive_PORT=8080
ENV DEPLOYMENT_RECEIVE_PORT=8081

ENV PEER_UPDATE_PORT=30001
ENV PEER_DEPLOYMENT_PORT=30002
ENV IPERF_DEST_PORT=30003

ENV NETWORK_INTERVAL=20
ENV PEER_UPDATE_INTERVAL=10
ENV DECISION_INTERVAL=20

# environment variables for different file path
ENV NETWORK_LOG=/code/network.csv
ENV LOCAL_METRIC_LOG=/code/local_metric.csv
ENV METRIC_LOG=/code/metric.csv
ENV DECISION_LOG=/code/decision.txt
ENV DEPLOYMENT_LOG=/code/deployment.log

# the list of all clusters in this "Edge network"
ENV CLUSTER_1_SUBNET="10.200.31.0/24" \
    CLUSTER_1_URL="10.200.31.10" \
    CLUSTER_2_SUBNET="10.200.32.0/24" \
    CLUSTER_2_URL="10.200.32.10" \
    CLUSTER_3_SUBNET="10.200.33.0/24" \
    CLUSTER_3_URL="10.200.33.10"


WORKDIR /code 

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano curl jq sysbench iputils-ping iperf uvicorn && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/ && \
    apt-get clean

COPY requirements.txt /code/
RUN pip3 install -r /code/requirements.txt

COPY . /code/

# 8080 used for updating metric with peer, 8081 for receiving deployment requests
# EXPOSE 8080 8081 5201

# CMD bash -c "python3 process.py && python3 deploy.py && bash /code/update.sh"
# CMD bash -c "uvicorn update-test:app --reload --host 0.0.0.0 --port 8080 && bash /code/update.sh“
RUN chmod +x ./run.sh
CMD ./run.sh