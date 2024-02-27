FROM python:3.9

WORKDIR /code
# updating data server
COPY ./update.sh /code/update.sh
# updating peer, deployment
COPY ./run.sh /code/run.sh
COPY ./peer-update.py /code/peer-update.py
COPY ./receive-deployment.py /code/receive-deployment.py
COPY ./requirements.txt /code/requirements.txt

RUN apt update && \
    apt install -y nano curl jq iputils-ping iperf3 uvicorn && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# 8080 used for updating metric with peer, 8081 for receiving deployment requests
# EXPOSE 8080 8081 5201

# CMD bash -c "python3 process.py && python3 deploy.py && bash /code/update.sh"
# CMD bash -c "uvicorn update-test:app --reload --host 0.0.0.0 --port 8080 && bash /code/update.sh“
RUN chmod +x ./update.sh ./run.sh
CMD ./run.sh