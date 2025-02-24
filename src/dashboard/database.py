# src/dashboard/database.py
import duckdb
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


@st.cache_resource
def get_db_connection():
    """Initialize or get DuckDB connection"""
    try:
        return duckdb.connect(":memory:")
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None


@st.cache_data
def load_stock_data(_con):
    """Load sample stock data"""
    try:
        # Create test data with more dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq="B")  # Business days

        data = {
            "timestamp": dates,
            "ticker": ["AAPL"] * len(dates),
            "close_price": [100.0 + i * 0.5 for i in range(len(dates))],
            "volume": [1000000 + i * 10000 for i in range(len(dates))],
        }
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Error creating test data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def load_sp500_data(_con):
    """Load sample SP500 data"""
    return pd.DataFrame(columns=["date", "close"])
