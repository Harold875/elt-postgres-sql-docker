FROM apache/airflow:2.11.2-python3.12

RUN pip install "apache-airflow-providers-docker>=2.0.0,<3.0.0"

