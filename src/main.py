
from pathlib import Path
import csv
import json

# Import functions from analytics.py
from analytics import (
    align_series,
    calculate_period_return,
    calculate_relative_performance,
    calculate_base_100
)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print("Data source: Local CSV")
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    print(f"Market:{instrument['market']}")
    print(f"Market: {benchmark['market']}")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")

    # ==========================================
    # FUNCTION TESTS: Analytics
    # ==========================================

    print("\n=== FUNCTION TESTS ===")

    # 1. Alignment
    aligned_aapl, aligned_sp500 = align_series(
        instrument_prices,
        benchmark_prices
    )

    print(f"Common aligned dates    : {len(aligned_aapl)}")

    # 2. Returns
    aapl_return = calculate_period_return(aligned_aapl)
    sp500_return = calculate_period_return(aligned_sp500)

    rel_perf = calculate_relative_performance(
        aapl_return,
        sp500_return
    )

    print(f"AAPL period return      : {aapl_return:+.2f}%")
    print(f"SP500 period return     : {sp500_return:+.2f}%")
    print(f"Relative performance    : {rel_perf:+.2f} percentage points")

    # 3. Base 100
    aapl_base_100 = calculate_base_100(aligned_aapl)
    sp500_base_100 = calculate_base_100(aligned_sp500)

    print(
        f"AAPL Base 100 start     : "
        f"{aapl_base_100[0]['value']:.1f} | "
        f"end: {aapl_base_100[-1]['value']:.2f}"
    )

    print(
        f"SP500 Base 100 start    : "
        f"{sp500_base_100[0]['value']:.1f} | "
        f"end: {sp500_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
