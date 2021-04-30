FROM python:3.6.13
LABEL maintainer="Nur Rohman Widiyanto"

WORKDIR /opt/ml/iris

COPY . .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "iris_server.py"]
