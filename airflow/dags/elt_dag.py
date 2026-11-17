import os
import subprocess
from datetime import datetime

from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}


def run_elt_script():
    script_path = '/opt/airflow/elt/elt_script.py'
    result = subprocess.run(["python", script_path], capture_output=True,text=True)
    
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)


dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description="An ELT workflow with dbt",
    start_date=datetime(2026, 11, 17),
    catchup=False,
)


# t1 -> es tarea 1
t1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag
)

dbt_project_dir = os.environ["DBT_PROJECT_DIR"] # /home/user/project/custom_postgres
dbt_profile = os.environ["DBT_PROFILE"]         # /home/user/.dbt

t2 = DockerOperator(
    task_id="dbt_run",
    image="ghcr.io/dbt-labs/dbt-postgres:1.4.7",
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt"
    ],
    auto_remove=True,         # -> se usa el valor de (True y False) en versiones de airflow. (>=1.0.0, <3.1.0)
    # auto_remove="success",      # -> se usa este valor en versiones superiores (>=3.10, <4.0.0)
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source=dbt_project_dir,
              target='/dbt', type='bind'),
        Mount(source=dbt_profile,
              target='/root', type='bind'),
    ],
    dag=dag,
)


# Orden de ejecucion
t1 >> t2
