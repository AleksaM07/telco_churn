import os
import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

def export_to_parquet():
    engine = sa.create_engine(
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    df = pd.read_sql_table('telco_customer_churn', con=engine)
    df.to_parquet(os.getenv('PARQUET_PATH'), index=False)

if __name__ == '__main__':
    export_to_parquet()
    print("Exported table to Parquet")