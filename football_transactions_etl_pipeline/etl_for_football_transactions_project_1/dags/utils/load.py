
from datetime import datetime

import awswrangler as wr
import boto3
from airflow.models.variable import Variable

from utils.extract import generate_transactions


def load_data():
    """
    Loading the data a parquet format into the data lake.

    Args:
        df
        date_string: append the ingestion_date as prefix to the file name.

    Returns:
        None.
    """

    df_transactions = generate_transactions()
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    file_name = f"{date_string}_football_transactions_data.parquet"
    s3_path = f"s3://football-transactions/{file_name}"
    session = boto3.session.Session(
        aws_access_key_id=Variable.get("ACCESS_KEY"),
        aws_secret_access_key=Variable.get("SECRET_KEY"),
        region_name="eu-central-1"
    )

    wr.s3.to_parquet(
        df=df_transactions,
        path=s3_path,
        boto3_session=session,
        # mode="append",
        dataset=False
    )
