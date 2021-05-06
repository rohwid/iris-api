#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DROP DATABASE IF EXISTS iris_db;
    DROP ROLE IF EXISTS iris;
    CREATE USER iris;
    CREATE DATABASE iris_db;
    GRANT ALL PRIVILEGES ON DATABASE iris_db TO iris;
    \c iris_db
    CREATE TABLE CLASS_RESULT(
        ID SERIAL,
        METHOD VARCHAR (50) NOT NULL,
        ACCURACY NUMERIC NOT NULL
    );
EOSQL