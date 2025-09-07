import streamlit as st
import yfinance as yf
import time

# Core logic: fetch latest OHLC and calculate tail dominance
def fetch(ticker):
    time.sleep(1.5)  # Throttle to avoid rate limits
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
        tail = low - min(open_, close)

    bar_size = high - low
    tail_percent = (tail / bar_size) * 100 if bar_size > 0 else 0
    if tail_percent < 70 and tail_percent > -70: 
        tail_percent = 0

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
            color = "green" if chg > 0 else "red"
            st.markdown(
                f"<span style='color:{color}; font-weight:bold'>{name}:</span> "
                f"`{close:.2f}` <span style='color:{color}'>({chg:+.2f}, {pct:+.2f}%)</span> "
                f"Tail: `{tail:.1f}%`",
                unsafe_allow_html=True
            )

    # Currencies
    with st.expander("💱 Currencies", expanded=True):
        for name, ticker in currencies.items():
            _, close, chg, pct, tail = fetch(ticker)
            color = "green" if chg > 0 else "red"
            st.markdown(
                f"<span style='color:{color}; font-weight:bold'>{name}:</span> "
                f"`{close:.4f}` <span style='color:{color}'>({chg:+.4f}, {pct:+.2f}%)</span> "
                f"Tail: `{tail:.1f}%`",
                unsafe_allow_html=True
            )

    # Commodities
    with st.expander("🛢️ Commodities", expanded=True):
        for name, ticker in commodities.items():
            _, close, chg, pct, tail = fetch(ticker)
            color = "green" if chg > 0 else "red"
            st.markdown(
                f"<span style='color:{color}; font-weight:bold'>{name}:</span> "
                f"`{close:.2f}` <span style='color:{color}'>({chg:+.2f}, {pct:+.2f}%)</span> "
                f"Tail: `{tail:.1f}%`",
                unsafe_allow_html=True
            )



