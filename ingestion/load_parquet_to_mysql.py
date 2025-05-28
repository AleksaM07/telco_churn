#pip install pyarrow fastparquet cryptography pymysql
import os, glob, pymysql
import pandas as pd
from sqlalchemy import create_engine
import pymysql

conn = pymysql.connect(host='localhost', user='aleksa', password='aleksa')
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS scilit_db")
conn.close()

pattern = os.path.join('../data/raw/', 'crossref_*.parquet')
parquet_files = glob.glob(pattern)
df_list = [pd.read_parquet(file) for file in parquet_files]
df_all = pd.concat(df_list, ignore_index=True)

# Connect to MySQL
engine = create_engine('mysql+pymysql://root:aleksa@localhost:3306/scilit_db')
df_all.to_sql('raw_crossref_parquet', con=engine, if_exists='replace', index=False)