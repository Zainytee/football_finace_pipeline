import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models.variable import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import \
    S3ToRedshiftOperator

from utils.extract import generate_transactions
from utils.load import load_data

os.environ['AWS_ACCESS_KEY_ID'] = Variable.get("ACCESS_KEY")
os.environ['AWS_SECRET_ACCESS_KEY'] = Variable.get("SECRET_KEY")

default_args = {
    "owner": "zainab",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(seconds=10),
}

my_dag = DAG(
    dag_id="etl_pipeline_faker_to_s3",
    default_args=default_args,
    description=(
        "An ETL pipeline for extracting from "
        "an faker generated data and loading into s3 bucket"),
    schedule_interval="@daily",
    start_date=datetime(2025, 7, 30)
)

extract_task = PythonOperator(
    dag=my_dag,
    python_callable=generate_transactions,
    task_id="extract_data"
)


load_task = PythonOperator(
    dag=my_dag,
    python_callable=load_data,
    task_id="load_data"
)

transfer_s3_to_redshift = S3ToRedshiftOperator(
    task_id="transfer_s3_to_redshift",
    aws_conn_id="aws_default",
    redshift_data_api_kwargs={
        "database": 'football_db',
        "cluster_identifier": 'tf-redshift-cluster',
        "db_user": 'redshiftcluster',
        "wait_for_completion": True,
    },
    s3_bucket='football-transactions',
    s3_key='{{ ds }}_football_transactions_data.parquet',
    schema="PUBLIC",
    table='football_transactions',
    copy_options=["FORMAT AS PARQUET"],
)

extract_task >> load_task >> transfer_s3_to_redshift
