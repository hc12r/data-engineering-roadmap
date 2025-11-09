"""
Example Airflow DAG: Simple Ingestion
"""
from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
except Exception:  # pragma: no cover
    DAG = object  # type: ignore
    def EmptyOperator(task_id: str):  # type: ignore
        return None


def create_dag():
    if DAG is object:
        return None

    with DAG(
        dag_id="ingestion_dag",
        start_date=datetime(2024, 1, 1),
        schedule_interval="@daily",
        catchup=False,
        tags=["ingestion", "example"],
    ) as dag:
        start = EmptyOperator(task_id="start")
        fetch = EmptyOperator(task_id="fetch_data")
        stage = EmptyOperator(task_id="stage_raw")
        end = EmptyOperator(task_id="end")

        start >> fetch >> stage >> end
        return dag


dag = create_dag()
