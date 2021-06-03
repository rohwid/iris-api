FROM python:3.6-slim-buster as base
LABEL maintainer="Nur Rohman Widiyanto"

# Using base 
FROM base as builder 

COPY ./requirements.txt ./scripts/install.sh ./
RUN ./install.sh && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

FROM base

COPY --from=builder /opt/venv /opt/venv

WORKDIR /opt/ml/iris

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "iris_server.py" ]

