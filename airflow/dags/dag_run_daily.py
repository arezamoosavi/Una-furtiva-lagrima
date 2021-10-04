from __future__ import print_function

from datetime import datetime

import airflow
from airflow.operators.bash_operator import BashOperator

args = {
    "owner": "airflow",
    "provide_context": True,
    "catchup": False,
}

dag = airflow.DAG(
    dag_id="daily_etl",
    default_args=args,
    start_date=datetime(year=2021, month=9, day=19),
    schedule_interval="0 07 * * *",
    max_active_runs=1,
    concurrency=1,
)

start_task = BashOperator(
    task_id="start_task",
    queue='default',
    bash_command="echo daily ETL for today_date: {{ ds }}",
    dag=dag,
)

start_task

# get yesterday data py op
# do partition postgres op