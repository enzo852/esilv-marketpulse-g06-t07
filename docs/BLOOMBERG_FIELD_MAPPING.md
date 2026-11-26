# Bloomberg Field Mapping

## 1. Access Mode

**Selected access mode: `APPROVED_SAMPLE`**

This TD09 documentation is based on the instructor-approved sample fixture.

Source files:

- `data/sample/bloomberg_reference_sample.json`
- `data/sample/bloomberg_reference_expected.json`

The sample is an educational fallback based on values from `data/sample/prices.csv`.

**Important:** This fixture does not demonstrate a live Bloomberg connection. The data must not be presented as verified historical Bloomberg market data.

The source keys inspected in the JSON file are teaching wrapper keys, not verified Bloomberg field mnemonics.

## 2. Bloomberg Identifiers

The following provider identifiers are associated with the MarketPulse canonical tickers:

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | `AAPL` | `AAPL US Equity` |
| Benchmark | `SP500` | `SPX Index` |

The mapping is:

- `AAPL` → `AAPL US Equity`
- `SP500` → `SPX Index`

**Important:** Bloomberg identifiers are provider-specific identifiers. They must not replace the canonical tickers used by MarketPulse.

## 3. Input Structure

The input file is:

`data/sample/bloomberg_reference_sample.json`

It contains two data series:

- An instrument series identified by `AAPL US Equity`
- A benchmark series identified by `SPX Index`

Each series contains:

- `canonical_ticker`
- `provider_identifier`
- An observations collection

Each observation contains the following source fields:

- `observation_date`
- `open_value`
- `high_value`
- `low_value`
- `close_value`
- `volume_value`

The sample contains 21 observations for each series, covering the period from September 1, 2026 to September 30, 2026.

These field names describe the educational JSON structure. They are not verified Bloomberg field mnemonics.

## 4. Field Mapping

The source fields must be mapped to the canonical MarketPulse fields as follows:

| Canonical field | Source field | Description |
|---|---|---|
| `date` | `observation_date` | Observation date |
| `ticker` | `canonical_ticker` | Canonical instrument identifier |
| `open` | `open_value` | Opening price |
| `high` | `high_value` | Highest price |
| `low` | `low_value` | Lowest price |
| `close` | `close_value` | Closing price |
| `volume` | `volume_value` | Trading volume |

The mapping applies to both the instrument and the benchmark.

The canonical `ticker` must be obtained from the parent series' `canonical_ticker` field.

The `provider_identifier` field is used to identify the provider instrument. It must not be used as the canonical ticker.

## 5. Missing Fields and Special Cases

The inspected sample provides all six source values required for the canonical row structure.

No missing canonical source field has been identified in the inspected fixture.

One special case concerns the benchmark series: its `volume_value` is equal to zero in the supplied sample.

This value must be preserved as supplied. It must not automatically be interpreted as a missing value.

No additional Bloomberg fields or Bloomberg mnemonics have been verified.

## 6. Canonical Output Structure

Each normalized MarketPulse observation must follow this structure:

```python
{
    "date": "...",
    "ticker": "AAPL",
    "open": ...,
    "high": ...,
    "low": ...,
    "close": ...,
    "volume": ...
}
```

For the benchmark series, the canonical ticker must be `SP500`.

The normalized data must preserve the canonical MarketPulse structure independently of the provider-specific identifiers.

TD09 documents the mapping. The actual normalization implementation belongs to TD10.

## 7. TD10 Handoff

The following information must be used when implementing the Bloomberg provider in TD10:

| Item | Expected value |
|---|---|
| Access mode | `APPROVED_SAMPLE` |
| Instrument identifier | `AAPL US Equity` |
| Instrument canonical ticker | `AAPL` |
| Benchmark identifier | `SPX Index` |
| Benchmark canonical ticker | `SP500` |
| Date source field | `observation_date` |
| Input format | JSON |
| Number of instrument observations | 21 |
| Number of benchmark observations | 21 |
| Expected canonical reference | `data/sample/bloomberg_reference_expected.json` |

Normalization requirements:

1. Read the two series from the JSON input.
2. Map the source observation fields to the canonical MarketPulse fields.
3. Derive the canonical ticker from `canonical_ticker`.
4. Preserve the provider identifiers separately from canonical tickers.
5. Preserve the benchmark volume value of zero.
6. Compare the normalized output with the expected canonical reference.

The expected reference contains 42 canonical rows: 21 for `AAPL` and 21 for `SP500`.

## 8. Validation Checklist

- [x] Access mode explicitly set to `APPROVED_SAMPLE`
- [x] Instrument mapping documented: `AAPL` → `AAPL US Equity`
- [x] Benchmark mapping documented: `SP500` → `SPX Index`
- [x] Input JSON structure inspected
- [x] Source fields mapped to canonical fields
- [x] Canonical tickers preserved
- [x] Teaching wrapper keys distinguished from Bloomberg field mnemonics
- [x] Missing fields and special cases documented
- [x] No live Bloomberg connectivity claimed
- [x] No credentials or sensitive session information included
- [x] TD10 handoff documented

**TD09 scope:** This document defines the Bloomberg field mapping contract. It does not implement the Bloomberg provider.