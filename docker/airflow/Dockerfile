FROM apache/airflow:2.0.0-python3.7

USER root

# INSTALL TOOLS
RUN apt-get update \
    && apt-get -y install libaio-dev \
    && apt-get install postgresql-client

RUN mkdir extra

USER airflow

# COPY SQL SCRIPT
COPY scripts/check_init.sql ./extra/check_init.sql
COPY scripts/set_init.sql ./extra/set_init.sql

# ENTRYPOINT SCRIPT
COPY scripts/init.sh ./init.sh

EXPOSE 8080

ENTRYPOINT ["./init.sh"]