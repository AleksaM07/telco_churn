from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    'scilit_metadata_pipeline',
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False
) as dag:

    ingest = BashOperator(
        task_id='run_ingestion',
        bash_command="cd /opt/airflow/ingestion && python ingestion.py"
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command="cd /opt/airflow/dbt/scilit_case && dbt deps && dbt run --profiles-dir /opt/***/dbt"
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command="cd /opt/airflow/dbt/scilit_case && dbt test --profiles-dir /opt/***/dbt"
    )

    ingest >> dbt_run >> dbt_test
