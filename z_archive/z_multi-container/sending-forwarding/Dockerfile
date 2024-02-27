FROM python:alpine3.19

ENV UPDATE_INTERVAL=20
ENV PEER_UPDATE_PORT=30001
ENV IPERF_SERVER_PORT=5201

WORKDIR /code
COPY . /code

RUN pip3 install -r requirements.txt

CMD ./run.sh