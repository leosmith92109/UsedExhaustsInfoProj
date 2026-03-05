# MotoExhaust Finder

MotoExhaust is a static web app for researching motorcycle exhaust options by bike generation, comparing setups, and launching used-market searches.

This project now uses a **relational CSV pipeline** (external data files) and generates a large app dataset consumed by `index.html`.

## What Changed

- Data moved out of inline JS into CSV + generated JSON.
- Coverage includes USDM bikes from 2000+ for major brands:
  - Honda, Yamaha, Kawasaki, Suzuki, KTM, BMW, Ducati, Triumph, Harley-Davidson, Indian, Husqvarna, GasGas, Aprilia, Moto Guzzi.
- Bike records are stored in `make + model + generation + year range` format.
- Fitments are relation rows and include `verification_status`.
- App can filter by fitment status (`All`, `verified`, `candidate`).

## Directory Layout

- `index.html`: single-file UI app.
- `data/raw/bikes.csv`: bike generation objects.
- `data/raw/exhaust_products.csv`: exhaust product catalog.
- `data/raw/fitments.csv`: relation rows linking bikes to exhaust products.
- `data/raw/verified_fitments.csv`: optional curated verified overrides.
- `data/generated/exhaust_dataset.json`: app-ready dataset loaded by browser.
- `data/generated/dataset_stats.json`: summary stats.
- `scripts/refresh_data.py`: full refresh entrypoint.
- `scripts/generate_bikes.py`: builds USDM bikes catalog CSV.
- `scripts/seed_exhaust_products.py`: seeds exhaust product CSV.
- `scripts/generate_fitments.py`: creates fitment relations.
- `scripts/build_dataset.py`: joins relational CSVs into app JSON.
- `scripts/pull_sources.py`: snapshots source pages for manual verification workflow.
- `scripts/query_dataset.py`: CLI query helper.
- `WORKFLOW.md`: detailed maintenance workflow.

## Quick Start

1. Build data:

```powershell
python scripts\refresh_data.py
```

2. Run local server (required for browser `fetch`):

```powershell
python -m http.server 8000
```

3. Open:

`http://localhost:8000/`

## Optional Flags

- Pull source snapshots before rebuild:

```powershell
python scripts\refresh_data.py --pull-sources
```

- Build UI dataset with only verified fitments:

```powershell
python scripts\refresh_data.py --verified-only
```

## Data Integrity Rules

- Unknown numeric specs are strict nulls in CSV/JSON.
- Candidate fitments are explicitly labeled and should be verified before purchase.
- Verified fitments should be added to `data/raw/verified_fitments.csv` with source URL and check date.

## Query Example

```powershell
python scripts\query_dataset.py --make Yamaha --model R1 --status candidate --limit 10
```

## Notes

- Marketplace links are generated only when selecting a card in UI.
- Nominatim geocoding is used for ZIP -> map center with rate limiting and abort handling.
