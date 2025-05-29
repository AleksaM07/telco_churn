from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import psycopg2

def create_database_if_not_exists():
    # Connect to the default 'postgres' DB
    conn = psycopg2.connect(
        host='postgres',
        port=5432,
        user='airflow',
        password='airflow',
        dbname='postgres'  # Connect to default postgres DB to create other DBs
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'telco_churn';")
    exists = cur.fetchone()
    if not exists:
        cur.execute('CREATE DATABASE telco_churn;')
        print("Database 'telco_churn' created.")
    else:
        print("Database 'telco_churn' already exists.")

    cur.close()
    conn.close()

with open("/opt/airflow/migrations/migrate.sql") as f:
    sql_content = f.read()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='churn_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    create_db = PythonOperator(
        task_id='create_database',
        python_callable=create_database_if_not_exists
    )

    migrate = SQLExecuteQueryOperator(
        task_id="migrate",
        conn_id="postgres_default",
        sql=sql_content,
        hook_params={"schema": "telco_churn"},
        dag=dag,
    )

    load = BashOperator(
        task_id='load',
        bash_command='python /opt/airflow/etl/load_raw.py'
    )

    extract = BashOperator(
        task_id='extract',
        bash_command='python /opt/airflow/etl/export_parquet.py'
    )

    train = BashOperator(
        task_id='train',
        bash_command='python /opt/airflow/model/train_model.py'
    )

    serve = BashOperator(
        task_id='serve',
        bash_command='uvicorn api.main:app --reload'
    )

    migrate >> load >> extract >> train >> serve