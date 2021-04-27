#!/bin/bash

python ./iris_svm.py
python ./iris_logistic_regression.py
python ./iris_decission_tree.py

kill $(ps aux | grep 'iris_server' | awk '{print $2}')

python ./iris_server