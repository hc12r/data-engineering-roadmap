"""
Example Airflow DAG: Reconciliation Pipeline
This is a lightweight illustrative DAG skeleton. Adjust imports and default_args per your environment.
"""
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
except Exception:  # pragma: no cover - placeholder if Airflow isn't installed
    DAG = object  # type: ignore
    def EmptyOperator(task_id: str):  # type: ignore
        return None


def create_dag():
    default_args = {
        "owner": "data-eng",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }
    dag_id = "reconciliation_pipeline_dag"

    if DAG is object:
        return None

    with DAG(
        dag_id=dag_id,
        start_date=datetime(2024, 1, 1),
        schedule_interval="0 2 * * *",
        catchup=False,
        default_args=default_args,
        tags=["reconciliation", "example"],
    ) as dag:
        start = EmptyOperator(task_id="start")
        ingest = EmptyOperator(task_id="ingest_sources")
        transform = EmptyOperator(task_id="transform_match")
        reconcile = EmptyOperator(task_id="reconcile_and_flag")
        publish = EmptyOperator(task_id="publish_results")
        end = EmptyOperator(task_id="end")

        start >> ingest >> transform >> reconcile >> publish >> end
        return dag


dag = create_dag()
