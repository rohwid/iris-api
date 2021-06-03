FROM apache/airflow:2.1.0-python3.6

USER root

# INSTALL TOOLS
RUN apt-get update \
    && apt-get -y install libaio-dev \
    && apt-get install postgresql-client

RUN mkdir extra

# ENTRYPOINT SCRIPT
COPY scripts/start_airflow.sh ./start_airflow.sh

RUN chmod +x ./start_airflow.sh \
    && chown airflow: ./start_airflow.sh

USER airflow

# COPY SQL SCRIPT
COPY scripts/check_init.sql ./extra/check_init.sql
COPY scripts/set_init.sql ./extra/set_init.sql

EXPOSE 8080

ENTRYPOINT ["./start_airflow.sh"]

