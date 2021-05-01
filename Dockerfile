FROM python:3.6-slim-buster as base
LABEL maintainer="Nur Rohman Widiyanto"

# 
FROM base as builder 

COPY ./requirements.txt ./docker_scripts/install.sh ./
RUN ./install.sh && python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

FROM base

COPY --from=builder /opt/venv /opt/venv

WORKDIR /opt/ml/iris

COPY . .
RUN rm -r docker_scripts

ENV PATH="/opt/venv/bin:$PATH"

CMD ["uwsgi", "--ini", "service.ini"]