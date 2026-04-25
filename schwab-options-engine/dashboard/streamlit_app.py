import sqlite3
import pandas as pd
import streamlit as st
from config import DB_PATH

st.set_page_config(page_title="Schwab Options Engine", layout="wide")
st.title("Schwab Options Positioning + Volatility Imbalance Engine")

conn = sqlite3.connect(DB_PATH)

st.subheader("Latest Ticker Scores")
try:
    df = pd.read_sql_query("SELECT * FROM ticker_scores ORDER BY ts DESC LIMIT 200", conn)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.warning(f"No ticker scores yet: {e}")

st.subheader("Latest Contract Features")
try:
    cf = pd.read_sql_query("SELECT * FROM contract_features ORDER BY ts DESC, contract_score DESC LIMIT 300", conn)
    st.dataframe(cf, use_container_width=True)
except Exception as e:
    st.warning(f"No contract features yet: {e}")

st.subheader("Alerts")
try:
    al = pd.read_sql_query("SELECT * FROM alerts ORDER BY ts DESC LIMIT 100", conn)
    st.dataframe(al, use_container_width=True)
except Exception as e:
    st.warning(f"No alerts yet: {e}")
