# src/dashboard/database.py
import duckdb
import streamlit as st


@st.cache_resource
def get_db_connection():
    """Initialize or get DuckDB connection"""
    return duckdb.connect("stocks.db", read_only=False)


@st.cache_data
def load_stock_data(con):
    """Load stock data from S3 parquet files"""
    return con.execute(
        """
        SELECT 
            t as timestamp,
            T as ticker,
            c as close_price,
            h as high,
            l as low,
            o as open_price,
            v as volume,
            vw as vwap
        FROM read_parquet('s3://alp-airflow/stocks_feed/daily_stocks_parquet/*.parquet')
    """
    ).df()


@st.cache_data
def load_sp500_data(con):
    """Load SP500 data from S3 parquet files"""
    return con.execute(
        """
        SELECT 
            date,
            close
        FROM read_parquet('s3://alp-airflow/stocks_feed/fred_sp500_parquet/*.parquet')
    """
    ).df()
