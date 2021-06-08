from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

import json
import csv
import requests

# Set the default args
default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 3, 31),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "rohman@pacmannai.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# Define the DAG
with DAG(dag_id="forex_data_pipeline",  
        schedule_interval="@daily", 
        default_args=default_args, 
        catchup=False) as dag:

    # Implement the file sensors
    is_forex_currencies_file_available = FileSensor(
        task_id="is_forex_currencies_file_available",
        fs_conn_id="forex_path",
        filepath="forex_currencies.csv",
        poke_interval=5,
        timeout=20
    )

    # Implement the bash operator
    saving_rates = BashOperator(
        task_id="saving_rates",
        # Triple quotes in python 
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
        """
    )

    sending_email_notification = EmailOperator(
        task_id="sending_email",
        to="rohman@pacmannai.com",
        subject="forex_data_pipeline",
        html_content="<h2>The Forex Data Pipeline Succeeded</h2> <p>Congratulation, The deployment of \"forex_data_pipeline\" DAGs was succeeded.<p>"
    )

    is_forex_rates_available >> is_forex_currencies_file_available >> downloading_rates >> saving_rates >> creating_forex_rates_table >> forex_processing >> sending_email_notification
    