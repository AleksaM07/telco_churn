import subprocess
import psycopg2
import pytest

def test_load_raw_loads_data():
    # Run your ETL script as a subprocess
    result = subprocess.run(
        ["python", "/opt/airflow/etl/load_raw.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"ETL script failed: {result.stderr}"

    # Connect to the Postgres DB and check row count
    conn = psycopg2.connect(
        host='postgres',
        port=5432,
        user='airflow',
        password='airflow',
        dbname='postgres'  # Connect to default postgres DB to create other DBs
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM telco_customer_churn;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()

    # Assert minimum expected rows (e.g., your CSV has ~7000 rows)
    assert count > 6000, f"Too few rows loaded: {count}"