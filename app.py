import toga
from toga.style import Pack
from toga.style.pack import COLUMN
import yfinance as yf

class MarketCheck(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))

        self.result_label = toga.Label("Fetching latest close...", style=Pack(margin=5))
        fetch_button = toga.Button("Get Market Snapshot", on_press=self.get_market_data, style=Pack(margin=5))

        main_box.add(self.result_label)
        main_box.add(fetch_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def get_market_data(self, widget):
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
                tail = low - min(open_, close)

            bar_size = high - low
            tail_percent = (tail / bar_size) * 100 if bar_size > 0 else 0

            return close, change, pct, tail_percent, date

        # Indices
        dow, dow_chg, dow_pct, dow_tail, date = fetch("^DJI")
        sp, sp_chg, sp_pct, sp_tail, _ = fetch("^GSPC")
        nasdaq, nasdaq_chg, nasdaq_pct, nasdaq_tail, _ = fetch("^IXIC")
        rut, rut_chg, rut_pct, rut_tail, _ = fetch("^RUT")

        # Currencies
        eurusd, eurusd_chg, eurusd_pct, eurusd_tail, _ = fetch("EURUSD=X")
        usdjpy, usdjpy_chg, usdjpy_pct, usdjpy_tail, _ = fetch("JPY=X")
        gbpusd, gbpusd_chg, gbpusd_pct, gbpusd_tail, _ = fetch("GBPUSD=X")

        # Commodities
        oil, oil_chg, oil_pct, oil_tail, _ = fetch("CL=F")
        copper, copper_chg, copper_pct, copper_tail, _ = fetch("HG=F")

        self.result_label.text = (
            f"Market Close Date: {date}\n\n"
            f"📈 Indices:\n"
            f"  Dow Jones: {dow:.2f} ({dow_chg:+.2f}, {dow_pct:+.2f}%) Tail: {dow_tail:.1f}%\n"
            f"  S&P 500: {sp:.2f} ({sp_chg:+.2f}, {sp_pct:+.2f}%) Tail: {sp_tail:.1f}%\n"
            f"  Nasdaq: {nasdaq:.2f} ({nasdaq_chg:+.2f}, {nasdaq_pct:+.2f}%) Tail: {nasdaq_tail:.1f}%\n"
            f"  Russell 2000: {rut:.2f} ({rut_chg:+.2f}, {rut_pct:+.2f}%) Tail: {rut_tail:.1f}%\n\n"
            f"💱 Currencies:\n"
            f"  EUR/USD: {eurusd:.4f} ({eurusd_chg:+.4f}, {eurusd_pct:+.2f}%) Tail: {eurusd_tail:.1f}%\n"
            f"  USD/JPY: {usdjpy:.2f} ({usdjpy_chg:+.2f}, {usdjpy_pct:+.2f}%) Tail: {usdjpy_tail:.1f}%\n"
            f"  GBP/USD: {gbpusd:.4f} ({gbpusd_chg:+.4f}, {gbpusd_pct:+.2f}%) Tail: {gbpusd_tail:.1f}%\n\n"
            f"🛢️ Commodities:\n"
            f"  Oil (WTI): {oil:.2f} ({oil_chg:+.2f}, {oil_pct:+.2f}%) Tail: {oil_tail:.1f}%\n"
            f"  Copper: {copper:.2f} ({copper_chg:+.2f}, {copper_pct:+.2f}%) Tail: {copper_tail:.1f}%"
        )

def main():
    return MarketCheck()
