FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /root/.kube

COPY gaas ./gaas
COPY instance ./instance
COPY main.py .

CMD [ "python", "./main.py" ]
