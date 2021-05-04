FROM postgres:13.2-alpine
LABEL maintainer="Nur Rohman Widiyanto"

COPY ./scripts/init-iris-db.sh /docker-entrypoint-initdb.d/init-iris-db.sh

EXPOSE 5432