# src/dashboard/config.py
import os

# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET", "alp-airflow")
S3_STOCKS_PREFIX = os.getenv("S3_STOCKS_PREFIX", "stocks_feed/daily_stocks_parquet")
S3_SP500_PREFIX = os.getenv("S3_SP500_PREFIX", "stocks_feed/fred_sp500_parquet")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Data columns/schema
STOCK_COLUMNS = {
    "t": "timestamp",
    "T": "ticker",
    "c": "close_price",
    "h": "high",
    "l": "low",
    "o": "open_price",
    "v": "volume",
    "vw": "vwap",
}
