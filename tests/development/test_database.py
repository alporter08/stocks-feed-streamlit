# test_database.py
import os
import duckdb
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def test_db_connection():
    print("Testing database connection...")
    try:
        conn = duckdb.connect(database=":memory:", read_only=False)
        print("Basic connection successful")

        # Try installing extensions
        print("Installing extensions...")
        conn.sql("INSTALL httpfs;")
        conn.sql("LOAD httpfs;")
        conn.sql("INSTALL aws;")
        conn.sql("LOAD aws;")
        print("Extensions loaded successfully")

        conn.sql(
            f"""
            CREATE SECRET secret1 (
                TYPE S3,
                KEY_ID '{AWS_ACCESS_KEY_ID}',
                SECRET '{AWS_SECRET_ACCESS_KEY}',
                REGION 'us-east-2'
                    );
                    """
        )

        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def test_s3_query(conn):
    print("Testing S3 query...")
    try:
        # Use a minimal query first
        query = """
            SELECT *
            FROM read_parquet('s3://alp-airflow/stocks_feed/daily_stocks_parquet/*.parquet')
            LIMIT 5
        """
        print(f"Executing query: {query}")
        result = conn.sql(query)
        df = result.df()
        print("Query successful!")
        print("\nFirst few rows:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error querying S3: {e}")
        return None


if __name__ == "__main__":
    print("Starting database tests...")

    # Test connection
    conn = test_db_connection()
    if conn is not None:
        # Test query
        df = test_s3_query(conn)
