#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE airflow__extra_conf(
    conf_name VARCHAR (255) PRIMARY KEY,
    conf_value VARCHAR (255) NOT NULL
  );
EOSQL