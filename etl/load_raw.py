import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def load_csv_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT')
    )
    cur = conn.cursor()
    with open(os.getenv('CSV_PATH'), 'r') as f:
        # skip header and copy
        f.readline()
        cur.copy_expert("COPY telco_customer_churn FROM STDIN WITH CSV", f)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    load_csv_to_db()
    print("Loaded raw CSV into PostgreSQL")