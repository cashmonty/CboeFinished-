import sqlite3

import pandas as pd
import streamlit as st
from pandas.io.formats.style import Styler

from config import DB_PATH

st.set_page_config(page_title="Schwab Options Engine", layout="wide")

SECTOR_GROUPS = {
    "ETF - Broad Market": ["SPY", "QQQ", "IWM", "DIA", "EEM", "FXI", "ARKK"],
    "ETF - Sector": ["XLF", "XLE", "XLK", "XLV", "XLI", "XLP", "XLY", "XLU", "XLB", "XLC", "SMH", "SOXX", "KRE"],
    "ETF - Leveraged": ["TQQQ", "SQQQ", "UVXY"],
    "ETF - Macro": ["GLD", "SLV", "TLT", "HYG", "LQD", "USO", "VXX"],
    "Technology": [
        "AAPL", "MSFT", "NVDA", "AVGO", "ORCL", "CRM", "ADBE", "INTC", "CSCO", "QCOM",
        "AMAT", "MU", "PANW", "PLTR", "SHOP", "ARM", "ASML", "TXN", "ADI", "LRCX",
        "KLAC", "MSTR", "NOW", "SNOW", "CRWD", "DDOG", "MDB", "ZS", "TEAM", "NET",
        "ANET", "APP", "MRVL", "MCHP", "NXPI", "ON", "MPWR",
    ],
    "Communication": ["META", "GOOGL", "GOOG", "NFLX", "TMUS", "CMCSA", "DIS", "VZ", "T"],
    "Consumer Discretionary": [
        "AMZN", "TSLA", "UBER", "ABNB", "BKNG", "MELI", "PDD", "JD", "BABA", "HD",
        "LOW", "TGT", "SBUX", "MCD", "NKE", "ROST", "TJX", "MAR", "CMG", "YUM",
        "GM", "F",
    ],
    "Consumer Staples": ["WMT", "COST", "KO", "PEP", "PM", "MO", "PG", "CL", "KMB", "GIS", "MDLZ", "KHC", "EL"],
    "Healthcare": [
        "JNJ", "ABBV", "MRK", "PFE", "LLY", "AMGN", "UNH", "CI", "CVS", "HUM",
        "ISRG", "TMO", "DHR", "ABT", "MDT", "SYK", "BMY", "GILD", "REGN", "VRTX",
        "BSX", "MRNA", "BIIB",
    ],
    "Industrials": ["GE", "CAT", "DE", "HON", "UPS", "FDX", "BA", "LMT", "RTX", "NOC", "GD", "ETN", "EMR", "MMM", "DAL", "UAL"],
    "Financials": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "CB", "CME", "ICE", "SPGI", "MCO", "AXP", "V", "MA", "COF", "TRV", "PGR", "ALL", "AIG", "PYPL"],
    "Energy": ["XOM", "CVX", "COP", "OXY", "SLB", "EOG", "MPC", "PSX", "VLO", "KMI", "HAL", "FANG", "DVN"],
    "Utilities": ["SO", "DUK", "NEE", "AEP"],
    "Real Estate": ["AMT", "PLD", "EQIX", "O"],
    "Materials": ["FCX", "NEM", "LIN", "SHW", "APD"],
}

SECTOR_COLORS = {
    "ETF - Broad Market": "#0f766e",
    "ETF - Sector": "#0ea5a4",
    "ETF - Leveraged": "#155e75",
    "ETF - Macro": "#0c4a6e",
    "Technology": "#2563eb",
    "Communication": "#7c3aed",
    "Consumer Discretionary": "#db2777",
    "Consumer Staples": "#16a34a",
    "Healthcare": "#dc2626",
    "Industrials": "#ea580c",
    "Financials": "#0891b2",
    "Energy": "#b45309",
    "Utilities": "#65a30d",
    "Real Estate": "#7c2d12",
    "Materials": "#6d28d9",
    "Other": "#4b5563",
}

SYMBOL_TO_SECTOR = {
    symbol: sector
    for sector, symbols in SECTOR_GROUPS.items()
    for symbol in symbols
}


def instrument_type(symbol: str) -> str:
    sector = SYMBOL_TO_SECTOR.get(symbol.upper(), "Other")
    return "ETF/ETP" if sector.startswith("ETF") else "Stock"


def sector_of(symbol: str) -> str:
    return SYMBOL_TO_SECTOR.get(symbol.upper(), "Other")


def annotate_symbols(df: pd.DataFrame, symbol_col: str) -> pd.DataFrame:
    if df.empty or symbol_col not in df.columns:
        return df

    annotated = df.copy()
    insert_at = annotated.columns.get_loc(symbol_col) + 1
    annotated.insert(insert_at, "Type", annotated[symbol_col].map(instrument_type))
    annotated.insert(insert_at + 1, "Sector", annotated[symbol_col].map(sector_of))
    return annotated


def sector_cell_style(value: str) -> str:
    color = SECTOR_COLORS.get(value, SECTOR_COLORS["Other"])
    return f"background-color: {color}; color: white; font-weight: 600;"


def type_cell_style(value: str) -> str:
    if value == "ETF/ETP":
        return "background-color: #0f766e; color: white; font-weight: 700;"
    return "background-color: #374151; color: white; font-weight: 600;"


def style_table(df: pd.DataFrame) -> Styler:
    styler = df.style
    sector_cols = [col for col in ("Sector",) if col in df.columns]
    type_cols = [col for col in ("Type",) if col in df.columns]
    symbol_cols = [col for col in ("symbol", "underlying") if col in df.columns]

    if sector_cols:
        styler = styler.map(sector_cell_style, subset=sector_cols)
    if type_cols:
        styler = styler.map(type_cell_style, subset=type_cols)
    if symbol_cols and "Sector" in df.columns:
        styler = styler.map(
            lambda value: sector_cell_style(sector_of(value)),
            subset=symbol_cols,
        )

    formatters = {
        "bullish_score": "{:.1f}",
        "bearish_score": "{:.1f}",
        "call_premium": "${:,.0f}",
        "put_premium": "${:,.0f}",
        "net_delta_notional": "${:,.0f}",
        "avg_iv_change": "{:.3f}",
        "premium_estimate": "${:,.0f}",
        "delta_notional": "${:,.0f}",
        "liquidity_score": "{:.1f}",
        "activity_score": "{:.1f}",
        "contract_score": "{:.1f}",
        "score": "{:.1f}",
    }
    active_formatters = {col: fmt for col, fmt in formatters.items() if col in df.columns}
    if active_formatters:
        styler = styler.format(active_formatters)

    return styler


def load_latest_ticker_scores(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        WITH ranked AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY ts DESC, id DESC) AS rn
            FROM ticker_scores
        )
        SELECT
            ts,
            symbol,
            bullish_score,
            bearish_score,
            call_premium,
            put_premium,
            net_delta_notional,
            call_volume_new,
            put_volume_new,
            avg_iv_change,
            underlying_trend_score,
            top_reason
        FROM ranked
        WHERE rn = 1
        ORDER BY bullish_score DESC, bearish_score DESC, symbol
    """
    return pd.read_sql_query(query, conn)


st.title("Schwab Options Positioning + Volatility Imbalance Engine")
st.caption("Tickers are color-coded by sector. ETFs and similar exchange-traded products are labeled as ETF/ETP.")

legend_html = "".join(
    f"<span style='display:inline-block;margin:0 0.45rem 0.45rem 0;padding:0.35rem 0.65rem;border-radius:999px;background:{color};color:white;font-size:0.85rem;font-weight:700;'>{sector}</span>"
    for sector, color in SECTOR_COLORS.items()
    if sector != "Other"
)
st.markdown(legend_html, unsafe_allow_html=True)

conn = sqlite3.connect(DB_PATH)

st.subheader("Latest Ticker Scores")
try:
    ticker_scores = annotate_symbols(load_latest_ticker_scores(conn), "symbol")

    sector_options = sorted(ticker_scores["Sector"].unique())
    type_options = sorted(ticker_scores["Type"].unique())
    filters_col1, filters_col2 = st.columns([2, 1])
    selected_sectors = filters_col1.multiselect(
        "Sectors",
        options=sector_options,
        default=sector_options,
    )
    selected_types = filters_col2.multiselect(
        "Instrument Type",
        options=type_options,
        default=type_options,
    )

    filtered_scores = ticker_scores[
        ticker_scores["Sector"].isin(selected_sectors)
        & ticker_scores["Type"].isin(selected_types)
    ]

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Visible Tickers", len(filtered_scores))
    metric_col2.metric("Stocks", int((filtered_scores["Type"] == "Stock").sum()))
    metric_col3.metric("ETF/ETPs", int((filtered_scores["Type"] == "ETF/ETP").sum()))

    st.dataframe(
        style_table(filtered_scores),
        width="stretch",
        hide_index=True,
        column_config={
            "ts": "Updated",
            "symbol": "Ticker",
            "bullish_score": st.column_config.NumberColumn("Bull", format="%.1f"),
            "bearish_score": st.column_config.NumberColumn("Bear", format="%.1f"),
            "call_premium": st.column_config.NumberColumn("Call Premium", format="$%.0f"),
            "put_premium": st.column_config.NumberColumn("Put Premium", format="$%.0f"),
            "net_delta_notional": st.column_config.NumberColumn("Net Delta", format="$%.0f"),
            "avg_iv_change": st.column_config.NumberColumn("Avg IV Change", format="%.3f"),
            "call_volume_new": "New Call Vol",
            "put_volume_new": "New Put Vol",
            "underlying_trend_score": "Trend",
            "top_reason": "Top Reason",
        },
    )
except Exception as e:
    st.warning(f"No ticker scores yet: {e}")

st.subheader("Latest Contract Features")
try:
    contract_features = pd.read_sql_query(
        "SELECT * FROM contract_features ORDER BY ts DESC, contract_score DESC LIMIT 300",
        conn,
    )
    contract_features = annotate_symbols(contract_features, "underlying")
    st.dataframe(
        style_table(contract_features),
        width="stretch",
        hide_index=True,
        column_config={
            "ts": "Updated",
            "underlying": "Ticker",
            "premium_estimate": st.column_config.NumberColumn("Premium", format="$%.0f"),
            "delta_notional": st.column_config.NumberColumn("Delta Notional", format="$%.0f"),
            "liquidity_score": st.column_config.NumberColumn("Liquidity", format="%.1f"),
            "activity_score": st.column_config.NumberColumn("Activity", format="%.1f"),
            "contract_score": st.column_config.NumberColumn("Contract Score", format="%.1f"),
        },
    )
except Exception as e:
    st.warning(f"No contract features yet: {e}")

st.subheader("Alerts")
try:
    alerts = pd.read_sql_query("SELECT * FROM alerts ORDER BY ts DESC LIMIT 100", conn)
    alerts = annotate_symbols(alerts, "symbol")
    st.dataframe(
        style_table(alerts),
        width="stretch",
        hide_index=True,
        column_config={
            "ts": "Updated",
            "symbol": "Ticker",
            "score": st.column_config.NumberColumn("Score", format="%.1f"),
            "price_at_alert": st.column_config.NumberColumn("Price", format="$%.2f"),
            "sent": st.column_config.CheckboxColumn("Sent"),
        },
    )
except Exception as e:
    st.warning(f"No alerts yet: {e}")
