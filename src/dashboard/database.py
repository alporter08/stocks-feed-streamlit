# src/dashboard/database.py
import duckdb
import streamlit as st
import pandas as pd
from dashboard.config import S3_BUCKET, S3_STOCKS_PREFIX, S3_SP500_PREFIX, STOCK_COLUMNS


@st.cache_resource
def get_db_connection():
    """Initialize or get DuckDB connection"""
    try:
        con = duckdb.connect("stocks.db", read_only=False)

        # Test connection with sample data
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS test_stocks AS 
            SELECT * FROM (
                VALUES 
                ('2024-02-23'::TIMESTAMP, 'AAPL', 100.0, 101.0, 99.0, 99.5, 1000000, 100.2),
                ('2024-02-22'::TIMESTAMP, 'AAPL', 99.5, 100.0, 98.0, 98.5, 1100000, 99.1)
            ) AS t(timestamp, ticker, close_price, high, low, open_price, volume, vwap)
        """
        )
        return con
    except Exception as e:
        st.error(f"Failed to connect to database: {str(e)}")
        raise


@st.cache_data
def load_stock_data(con):
    """Load stock data from S3 parquet files"""
    try:
        # First try S3
        query = f"""
            SELECT 
                t as timestamp,
                T as ticker,
                c as close_price,
                h as high,
                l as low,
                o as open_price,
                v as volume,
                vw as vwap
            FROM read_parquet(
                's3://{S3_BUCKET}/{S3_STOCKS_PREFIX}/*.parquet'
            )
        """
        return con.execute(query).df()
    except Exception as e:
        st.warning("Failed to load S3 data, falling back to test data")
        return con.execute("SELECT * FROM test_stocks").df()


@st.cache_data
def load_sp500_data(con):
    """Load SP500 data from S3 parquet files"""
    try:
        query = f"""
            SELECT 
                date,
                close
            FROM read_parquet(
                's3://{S3_BUCKET}/{S3_SP500_PREFIX}/*.parquet'
            )
        """
        return con.execute(query).df()
    except Exception as e:
        st.warning("Failed to load S3 SP500 data")
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=["date", "close"])
