FROM alpine:3.19

ENV UPDATE_INTERVAL=20
ENV PEER_UPDATE_PORT=8001
ENV IPERF_SERVER_PORT=5201

#ENV CLUSTER_1_SUBNET="10.200.31.0/24" \
#    CLUSTER_1_URL="http://10.200.31.10" \
#    CLUSTER_2_SUBNET="10.200.32.0/24" \
#    CLUSTER_2_URL="http://10.200.32.10" \
#    CLUSTER_3_SUBNET="10.200.33.0/24" \
#    CLUSTER_3_URL="http://10.200.33.10"

ENV DATA_SERVER_IP=10.200.30.10
ENV DATA_SERVER_PORT=20000

#ENV NETWORK_LOG=/code/local/network.cvs
#ENV METRIC_LOG=/code/local/metric.cvs

WORKDIR /code
COPY . /code

RUN apk add iperf curl jq sysbench
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN chmod +x /code/run.sh /code/resource.sh /code/network.sh

CMD /code/run.sh