FROM apache/airflow:2.10.3

WORKDIR /airflow

COPY requirement.txt airflow/requirement.txt

RUN pip install --retries 5 --timeout 60 --no-cache-dir -r airflow/requirement.txt

