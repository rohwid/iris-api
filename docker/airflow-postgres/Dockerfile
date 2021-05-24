FROM postgres:13.2-alpine
LABEL maintainer="Nur Rohman Widiyanto"

COPY ./scripts/init_db.sh /docker-entrypoint-initdb.d/init_db.sh

EXPOSE 5432