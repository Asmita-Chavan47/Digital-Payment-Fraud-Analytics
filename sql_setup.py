import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()


DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS") 
DB_HOST = "localhost"

temp_engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/")
with temp_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS fraud_detection"))
print("Database Created!")

df = pd.read_csv("fraud_dashboard_data.csv")
print(f"{len(df)} rows")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/fraud_detection")

df.to_sql("transactions", con=engine, if_exists="replace", index=False, chunksize=5000)

with engine.connect() as conn:
    result = conn.execute(text("SELECT Class, COUNT(*) as total FROM transactions GROUP BY Class"))
    for row in result:
        print(row)