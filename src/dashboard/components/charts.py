# src/dashboard/components/charts.py
import plotly.express as px
import streamlit as st


def plot_price_movement(df, ticker):
    """Plot price movement over time"""
    fig = px.line(df, x="timestamp", y="close_price", title=f"{ticker} Price Movement")
    return st.plotly_chart(fig, use_container_width=True)


def plot_volume(df, ticker):
    """Plot trading volume"""
    fig = px.bar(df, x="timestamp", y="volume", title=f"{ticker} Trading Volume")
    return st.plotly_chart(fig, use_container_width=True)


def plot_price_vs_vwap(df, ticker):
    """Plot price vs VWAP comparison"""
    fig = px.line(
        df, x="timestamp", y=["close_price", "vwap"], title=f"{ticker} Price vs VWAP"
    )
    return st.plotly_chart(fig, use_container_width=True)
