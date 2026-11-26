from pathlib import Path
import json

if __package__:
    # Cas 1 : import depuis la racine du projet (TD11)
    from .analytics import (
        align_series,
        calculate_period_return,
        calculate_relative_performance,
        calculate_base_100
    )

    from .providers.bloomberg_provider import (
        fetch_bloomberg_prices,
        ACCESS_MODE
    )

else:
    # Cas 2 : exécution directe de main.py
    from analytics import (
        align_series,
        calculate_period_return,
        calculate_relative_performance,
        calculate_base_100
    )

    from providers.bloomberg_provider import (
        fetch_bloomberg_prices,
        ACCESS_MODE
    )

# ============================================================
# 1. APPLICATION SETTINGS
# ============================================================

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "sample"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

PROVIDER_NAME = "Bloomberg stage"


# ============================================================
# 2. LOAD INSTRUMENT INFORMATION
# ============================================================

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# 3. SHARED APPLICATION SNAPSHOT (TD10)
# ============================================================

def build_market_snapshot(
    instrument_ticker="AAPL",
    benchmark_ticker="SP500"
):
    """
    Build the shared MarketPulse application snapshot.

    This function retrieves Bloomberg canonical rows,
    aligns the two series and reuses shared analytics.

    Returns:
        dict: Shared application result for terminal and dashboard.
    """

    # 1. Load instrument metadata
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # 2. Retrieve Bloomberg canonical rows
    instrument_prices = fetch_bloomberg_prices(
        instrument_ticker,
        mode=ACCESS_MODE
    )

    benchmark_prices = fetch_bloomberg_prices(
        benchmark_ticker,
        mode=ACCESS_MODE
    )

    # 3. Validate provider output
    if not instrument_prices:
        raise ValueError("Bloomberg returned no instrument observations.")

    if not benchmark_prices:
        raise ValueError("Bloomberg returned no benchmark observations.")

    # 4. Align common dates (TD07)
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices
    )

    if not aligned_instrument or not aligned_benchmark:
        raise ValueError("No common dates between instrument and benchmark.")

    # 5. Calculate period returns (TD07)
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    # 6. Calculate relative performance (TD07)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return
    )

    # 7. Calculate Base 100 (TD07)
    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    # 8. Return shared application result
    return {
        "provider": PROVIDER_NAME,
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": {
            **instrument,
            "ticker": instrument_ticker,
            "prices": aligned_instrument,
        },
        "benchmark": {
            **benchmark,
            "ticker": benchmark_ticker,
            "prices": aligned_benchmark,
        },
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


# ============================================================
# 4. TERMINAL PRESENTATION
# ============================================================

def main():

    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    instrument_prices = instrument["prices"]
    benchmark_prices = benchmark["prices"]

    print("=" * 50)
    print("              MarketPulse")
    print("=" * 50)

    print("\nProvider")
    print(snapshot["provider"])

    print("\nAccess mode")
    print(snapshot["access_mode"])

    print("\nInstrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_prices[-1]['close']}")

    print("\nBenchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_prices[-1]['close']}")

    print("\nMarket context")
    print(f"Period: {snapshot['lookback']}")
    print(f"Interval: {snapshot['interval']}")

    print("\nObservations")
    print(f"Instrument: {len(instrument_prices)}")
    print(f"Benchmark: {len(benchmark_prices)}")
    print(f"Common dates: {len(instrument_prices)}")

    print("\nPerformance")
    print(f"Instrument return: {snapshot['instrument_return']:+.2f}%")
    print(f"Benchmark return: {snapshot['benchmark_return']:+.2f}%")
    print(
        f"Relative performance: "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )

    print("\nBase 100")
    print(
        f"Instrument: "
        f"{snapshot['instrument_base_100'][0]['value']:.2f} "
        f"-> {snapshot['instrument_base_100'][-1]['value']:.2f}"
    )

    print(
        f"Benchmark: "
        f"{snapshot['benchmark_base_100'][0]['value']:.2f} "
        f"-> {snapshot['benchmark_base_100'][-1]['value']:.2f}"
    )

    print("\n" + "=" * 50)


# ============================================================
# 5. IMPORT-SAFE ENTRY POINT (TD11)
# ============================================================

if __name__ == "__main__":
    main()
