FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY run.sh run.sh

COPY main.py main.py
RUN chmod +x run.sh

CMD ./run.sh