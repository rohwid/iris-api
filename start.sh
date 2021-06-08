#!/bin/bash

cp ml/iris/requirements.txt docker/iris-server

sudo docker-compose up --detach --build

