#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  \c iris_db
  CREATE TABLE CLASS_RESULT(
    ID SERIAL,
    METHOD VARCHAR (50) NOT NULL,
    ACCURACY NUMERIC NOT NULL
  );
EOSQL