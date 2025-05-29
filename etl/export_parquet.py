import os
import pandas as pd
import polars as pl
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

def export_to_parquet_fast():
    engine = sa.create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    # Step 1: Load with Pandas
    df_pd = pd.read_sql_table('telco_customer_churn', con=engine)

    # Step 2: Convert to Polars
    df_pl = pl.from_pandas(df_pd)

    # Step 3: Save to Parquet
    df_pl.write_parquet(os.getenv('PARQUET_PATH'))
    print(f"Exported {df_pl.shape[0]} rows to {os.getenv('PARQUET_PATH')} using Polars")

if __name__ == '__main__':
    export_to_parquet_fast()
