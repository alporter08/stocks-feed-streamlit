import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from dashboard.database import get_db_connection, load_stock_data, load_sp500_data


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
        min_date = stocks_df["timestamp"].min().date()
        max_date = stocks_df["timestamp"].max().date()
        default_start = max_date - timedelta(days=7)

        date_range = st.sidebar.date_input(
            "Date Range",
            value=(default_start, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        # Filter data - fix the date filtering
        start_date = pd.Timestamp(date_range[0])
        end_date = pd.Timestamp(date_range[1])

        filtered_df = stocks_df[
            (stocks_df["ticker"] == selected_ticker)
            & (stocks_df["timestamp"].dt.date >= start_date.date())
            & (stocks_df["timestamp"].dt.date <= end_date.date())
        ].copy()  # Create a copy to avoid SettingWithCopyWarning

        if len(filtered_df) > 0:
            # Display metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                latest_price = filtered_df["close_price"].iloc[-1]
                st.metric("Latest Price", f"${latest_price:.2f}")

            with col2:
                price_change = latest_price - filtered_df["close_price"].iloc[0]
                st.metric("Price Change", f"${price_change:.2f}")

            with col3:
                volume = filtered_df["volume"].mean()
                st.metric("Avg Daily Volume", f"{volume:,.0f}")

            # Price chart
            st.subheader("Price Movement")
            fig = px.line(
                filtered_df,
                x="timestamp",
                y="close_price",
                title=f"{selected_ticker} Price Movement",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Volume chart
            st.subheader("Trading Volume")
            fig = px.bar(
                filtered_df,
                x="timestamp",
                y="volume",
                title=f"{selected_ticker} Trading Volume",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected date range")

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
