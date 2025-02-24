# src/dashboard/database.py
import duckdb
import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta
from dashboard.config import (
    S3_BUCKET,
    S3_STOCKS_PREFIX,
    S3_SP500_PREFIX,
    STOCK_COLUMNS,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def get_db_connection():
    """Initialize or get DuckDB connection"""
    try:
        # Try connecting with specific configuration
        conn = duckdb.connect(database=":memory:", read_only=False)
        # Install and load AWS extension
        conn.sql("INSTALL httpfs;")
        conn.sql("LOAD httpfs;")
        conn.sql("INSTALL aws;")
        conn.sql("LOAD aws;")

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
        logger.error(f"Database connection error: {e}")
        st.error(f"Database connection error: {str(e)}")
        return None


def create_test_data():
    """Create test data if S3 load fails"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq="B")

    data = {
        "timestamp": dates,
        "ticker": ["AAPL"] * len(dates),
        "close_price": [100.0 + i * 0.5 for i in range(len(dates))],
        "high": [101.0 + i * 0.5 for i in range(len(dates))],
        "low": [99.0 + i * 0.5 for i in range(len(dates))],
        "open_price": [99.5 + i * 0.5 for i in range(len(dates))],
        "volume": [1000000 + i * 10000 for i in range(len(dates))],
        "vwap": [100.2 + i * 0.5 for i in range(len(dates))],
    }
    logger.info("Created test data due to S3 load failure")
    return pd.DataFrame(data)


@st.cache_data
def load_stock_data(con):
    """Load stock data from S3"""
    if con is None:
        logger.error("No database connection available")
        return create_test_data()

    try:
        # Use column mapping from config
        columns_sql = ", ".join(
            [f"{col} as {name}" for col, name in STOCK_COLUMNS.items()]
        )

        query = f"""
            SELECT {columns_sql}
            FROM read_parquet(
                's3://{S3_BUCKET}/{S3_STOCKS_PREFIX}/*.parquet'
            )
        """
        logger.info(f"Executing query to load stock data from S3: {query}")
        df = con.execute(query).df()

        if len(df) == 0:
            logger.warning("No data found in S3")
            raise Exception("No data found in S3")

        logger.info(f"Successfully loaded {len(df)} rows of stock data")
        return df
    except Exception as e:
        logger.error(f"Failed to load S3 data: {e}")
        st.warning(f"Failed to load S3 data: {str(e)}, falling back to test data")
        return create_test_data()


@st.cache_data
def load_sp500_data(con):
    """Load SP500 data from S3"""
    if con is None:
        logger.error("No database connection available")
        return pd.DataFrame(columns=["date", "close"])

    try:
        query = f"""
            SELECT 
                date,
                value as close
            FROM read_parquet(
                's3://{S3_BUCKET}/{S3_SP500_PREFIX}/*.parquet'
            )
            WHERE value != '.'  -- Filter out missing values
            ORDER BY date
        """
        logger.info(f"Executing query to load SP500 data from S3: {query}")
        df = con.execute(query).df()

        if len(df) == 0:
            logger.warning("No SP500 data found in S3")
            raise Exception("No SP500 data found in S3")

        # Convert date to datetime if it's not already
        df["date"] = pd.to_datetime(df["date"])

        logger.info(f"Successfully loaded {len(df)} rows of SP500 data")
        return df
    except Exception as e:
        logger.error(f"Failed to load SP500 data: {e}")
        st.warning(f"Failed to load SP500 data: {str(e)}")
        return pd.DataFrame(columns=["date", "close"])


def validate_data(df, expected_columns):
    """Validate dataframe has expected columns and data"""
    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataframe: {missing_columns}")

    if len(df) == 0:
        raise ValueError("Dataframe is empty")

    return True
