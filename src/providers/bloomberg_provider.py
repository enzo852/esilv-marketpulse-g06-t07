
from pathlib import Path
import json


# ============================================================
# 1. CONSTANTS AND PATH RESOLUTION
# ============================================================

# Project root: MarketPulse/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

SAMPLE_PATH = PROJECT_ROOT / "data" / "sample" / "bloomberg_reference_sample.json"

EXPECTED_PATH = PROJECT_ROOT / "data" / "sample" / "bloomberg_reference_expected.json"

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

ACCESS_MODE = "APPROVED_SAMPLE"


def get_reference_sample_path():
    """Return the absolute path to the approved Bloomberg sample."""

    if SAMPLE_PATH.exists():
        return SAMPLE_PATH

    raise FileNotFoundError(
        f"Bloomberg reference sample not found: {SAMPLE_PATH}"
    )


# ============================================================
# 2. SAMPLE EXTRACTION
# ============================================================

def load_bloomberg_reference_sample(path=None):
    """Load the approved Bloomberg reference JSON."""

    target_path = Path(path) if path else get_reference_sample_path()

    if not target_path.exists():
        raise FileNotFoundError(
            f"Bloomberg sample file not found: {target_path}"
        )

    with open(target_path, encoding="utf-8") as file:
        return json.load(file)


def find_reference_series(payload, provider_identifier):
    """Find a series using its Bloomberg provider identifier."""

    for series in payload.get("series", []):
        if series.get("provider_identifier") == provider_identifier:
            return series

    raise ValueError(
        f"Approved Bloomberg series not found: {provider_identifier}"
    )


# ============================================================
# 3. NORMALIZATION
# ============================================================

def normalize_reference_series(series):
    """
    Convert Bloomberg teaching-wrapper observations
    into canonical MarketPulse rows.
    """

    canonical_ticker = series["canonical_ticker"]
    rows = []

    required_fields = [
        "observation_date",
        "open_value",
        "high_value",
        "low_value",
        "close_value",
        "volume_value",
    ]

    for index, obs in enumerate(series["observations"]):

        missing_fields = [
            field for field in required_fields
            if field not in obs
        ]

        if missing_fields:
            raise ValueError(
                f"Missing fields in {canonical_ticker}, "
                f"observation {index}: {missing_fields}"
            )

        rows.append({
            "date": obs["observation_date"],
            "ticker": canonical_ticker,
            "open": float(obs["open_value"]),
            "high": float(obs["high_value"]),
            "low": float(obs["low_value"]),
            "close": float(obs["close_value"]),
            "volume": int(obs["volume_value"]),
        })

    return rows


# ============================================================
# 4. APPROVED SAMPLE PROVIDER
# ============================================================

def fetch_approved_sample_prices(provider_identifier, sample_path=None):
    """Extract and normalize one approved Bloomberg series."""

    payload = load_bloomberg_reference_sample(sample_path)

    series = find_reference_series(
        payload,
        provider_identifier
    )

    return normalize_reference_series(series)


# ============================================================
# 5. LIVE BLOOMBERG ACCESS HOOK
# ============================================================

def fetch_raw_bloomberg_history(
    identifier,
    start_date=None,
    end_date=None
):
    """
    Placeholder for instructor-approved Bloomberg LIVE access.

    Actual implementation requires the dealing-room environment.
    """

    raise NotImplementedError(
        "Live Bloomberg access requires the instructor-approved "
        "dealing-room environment."
    )


# ============================================================
# 6. MAIN PROVIDER ENTRY POINT
# ============================================================

def fetch_bloomberg_prices(ticker, mode=ACCESS_MODE):
    """
    Fetch Bloomberg prices and return canonical MarketPulse rows.

    Supported tickers:
        AAPL
        SP500

    Supported modes:
        APPROVED_SAMPLE
        LIVE
    """

    if ticker not in BLOOMBERG_IDENTIFIERS:
        raise KeyError(
            f"Unknown canonical ticker for Bloomberg provider: {ticker}"
        )

    provider_identifier = BLOOMBERG_IDENTIFIERS[ticker]

    if mode == "APPROVED_SAMPLE":

        rows = fetch_approved_sample_prices(
            provider_identifier
        )

        return rows

    elif mode == "LIVE":

        return fetch_raw_bloomberg_history(
            provider_identifier
        )

    else:
        raise ValueError(
            f"Unrecognized Bloomberg mode: {mode}"
        )
