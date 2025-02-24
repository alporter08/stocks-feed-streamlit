# src/dashboard/components/metrics.py
import streamlit as st


def display_key_metrics(df):
    """Display key metrics in columns"""
    col1, col2, col3 = st.columns(3)

    with col1:
        latest_price = df["close_price"].iloc[-1]
        st.metric("Latest Price", f"${latest_price:.2f}")

    with col2:
        price_change = latest_price - df["close_price"].iloc[0]
        st.metric("Price Change", f"${price_change:.2f}")

    with col3:
        volume = df["volume"].mean()
        st.metric("Avg Daily Volume", f"{volume:,.0f}")
