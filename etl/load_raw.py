import os
import psycopg2
from dotenv import load_dotenv
import polars as pl
from io import StringIO

load_dotenv()

def get_env_var(key):
    val = os.getenv(key)
    if val:
        return val.strip()
    else:
        raise EnvironmentError(f"{key} not set")

def fill_all_nulls(df: pl.DataFrame) -> pl.DataFrame:
    for col_name, dtype in zip(df.columns, df.dtypes):
        for col_name, dtype in zip(df.columns, df.dtypes):
            if dtype == pl.Float64 or dtype == pl.Int64 or dtype == pl.Int32 or dtype == pl.Float32:
                df = df.with_columns(pl.col(col_name).fill_null(0))
            elif dtype == pl.Utf8: df = df.with_columns(pl.col(col_name).fill_null(''))
            elif dtype == pl.Boolean: df = df.with_columns(pl.col(col_name).fill_null(False))
            else: df = df.with_column(pl.col(col_name).fill_null(''))
        return df

def load_csv_to_db():
    df = pl.read_csv(get_env_var('CSV_PATH'), try_parse_dates=True)

    # Fill all NA values
    df = fill_all_nulls(df)

    csv_buffer = StringIO()
    df.write_csv(csv_buffer)
    csv_buffer.seek(0)

    conn = psycopg2.connect(
        dbname=get_env_var('POSTGRES_DB'),
        user=get_env_var('POSTGRES_USER'),
        password=get_env_var('POSTGRES_PASSWORD'),
        host=get_env_var('POSTGRES_HOST'),
        port=get_env_var('POSTGRES_PORT')
    )
    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE telco_customer_churn")

    cur.copy_expert("COPY telco_customer_churn FROM STDIN WITH CSV HEADER", csv_buffer)

    conn.commit()
    cur.close()
    conn.close()
    print("Polars-cleaned CSV loaded into PostgreSQL.")

if __name__ == '__main__':
    load_csv_to_db()