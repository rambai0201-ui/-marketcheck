import streamlit as st
import yfinance as yf

# Core logic: fetch latest OHLC and calculate tail dominance
def fetch(ticker):
    data = yf.Ticker(ticker).history(period="5d")
    latest = data.iloc[-1]
    date = data.index[-1].strftime("%Y-%m-%d")

    open_ = latest["Open"]
    high = latest["High"]
    low = latest["Low"]
    close = latest["Close"]
    prev_close = data["Close"][-2]

    change = close - prev_close
    pct = (change / prev_close) * 100

    mid = (high + low) / 2
    tail = 0
    if open_ < mid and close < mid:
        tail = high - max(open_, close)
    elif open_ > mid and close > mid:
        tail = min(open_, close) - low

    bar_size = high - low
    tail_percent = (tail / bar_size) * 100 if bar_size > 0 else 0

    return date, close, change, pct, tail_percent

# Asset groups
indices = {
    "Dow Jones": "^DJI",
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT"
}

currencies = {
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "GBP/USD": "GBPUSD=X"
}

commodities = {
    "Oil (WTI)": "CL=F",
    "Copper": "HG=F"
}

# Streamlit layout
st.set_page_config(page_title="Market Check", layout="centered")
st.title("📊 Market Check")
st.caption("Latest market snapshot with candle tail analysis")

if st.button("Get Market Data"):
    st.divider()
    date, *_ = fetch("^DJI")  # Use Dow to get the shared date
    st.markdown(f"**Market Close Date:** `{date}`")

    # Indices
    with st.expander("📈 Indices", expanded=True):
        for name, ticker in indices.items():
            _, close, chg, pct, tail = fetch(ticker)
            st.markdown(f"**{name}**: `{close:.2f}` ({chg:+.2f}, {pct:+.2f}%) Tail: `{tail:.1f}%`")

    # Currencies
    with st.expander("💱 Currencies", expanded=True):
        for name, ticker in currencies.items():
            _, close, chg, pct, tail = fetch(ticker)
            st.markdown(f"**{name}**: `{close:.4f}` ({chg:+.4f}, {pct:+.2f}%) Tail: `{tail:.1f}%`")

    # Commodities
    with st.expander("🛢️ Commodities", expanded=True):
        for name, ticker in commodities.items():
            _, close, chg, pct, tail = fetch(ticker)
            st.markdown(f"**{name}**: `{close:.2f}` ({chg:+.2f}, {pct:+.2f}%) Tail: `{tail:.1f}%`")
