# src/dashboard/app.py
import streamlit as st
from datetime import datetime, timedelta
from dashboard.database import get_db_connection, load_stock_data, load_sp500_data
from dashboard.components.charts import (
    plot_price_movement,
    plot_volume,
    plot_price_vs_vwap,
)
from dashboard.components.metrics import display_key_metrics


def main():
    st.title("Stock Market Dashboard")

    # Initialize DB connection
    con = get_db_connection()

    try:
        # Load data
        stocks_df = load_stock_data(con)
        sp500_df = load_sp500_data(con)

        # Sidebar filters
        st.sidebar.header("Filters")
        tickers = sorted(stocks_df["ticker"].unique())
        selected_ticker = st.sidebar.selectbox("Select Stock", tickers)

        # Date range
        max_date = stocks_df["timestamp"].max()
        min_date = stocks_df["timestamp"].min()
        date_range = st.sidebar.date_input(
            "Date Range",
            value=(max_date - timedelta(days=30), max_date),
            min_value=min_date,
            max_value=max_date,
        )

        # Filter data
        mask = (
            (stocks_df["ticker"] == selected_ticker)
            & (stocks_df["timestamp"].dt.date >= date_range[0])
            & (stocks_df["timestamp"].dt.date <= date_range[1])
        )
        filtered_df = stocks_df[mask]

        # Display components
        display_key_metrics(filtered_df)
        plot_price_movement(filtered_df, selected_ticker)
        plot_volume(filtered_df, selected_ticker)
        plot_price_vs_vwap(filtered_df, selected_ticker)

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
