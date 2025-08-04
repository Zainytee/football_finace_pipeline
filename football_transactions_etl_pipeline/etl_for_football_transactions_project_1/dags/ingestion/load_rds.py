import io

import pandas as pd
import psycopg2
from airflow.models import Variable
from sqlalchemy import create_engine

from ingestion.extract_2 import get_results

# event_df = get_results()


def load_to_rds():
    """
    A function that writes a DataFrame to an RDS PostgreSQL database.

    Arg: None

    Return: Successfully loaded message
    """
    df = get_results()
    print(df.head())
    username = Variable.get('rds_db_username')
    password = Variable.get('rds_db_password')
    host = Variable.get('endpoint')
    port = "5432"
    database = Variable.get('DB_NAME')

    engine = create_engine(
        f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    )
    df.to_sql('competitions', engine, if_exists='replace', index=False)

    return f"Data Successfully loaded. {df.shape[0]} rows and {df.shape[1]} columns loaded."
