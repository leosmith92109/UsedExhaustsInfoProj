# Data Refresh Workflow

This workflow keeps MotoExhaust data current and scalable while preserving strict unknown/null handling.

## 1) Pull latest source snapshots (optional but recommended)

```powershell
python scripts\pull_sources.py
```

Outputs:
- `data/raw/source_snapshots/*.html`
- `data/raw/source_snapshots/snapshot_index.csv`

Use these snapshots to validate product names/fitment claims before marking rows as verified.

## 2) Regenerate base relational CSVs

```powershell
python scripts\generate_bikes.py
python scripts\seed_exhaust_products.py
python scripts\generate_fitments.py
```

Or run all in one step:

```powershell
python scripts\refresh_data.py
```

## 3) Curate verified fitments

Edit:

`data/raw/verified_fitments.csv`

Columns:
- `fitment_id`
- `bike_id`
- `product_id`
- `fitment_year_start`
- `fitment_year_end`
- `verification_status` (`verified`)
- `source_url`
- `source_checked_on` (`YYYY-MM-DD`)
- `fitment_notes`

Behavior:
- Verified rows override candidate rows for the same bike/product/year range.

## 4) Build app dataset from relational files

```powershell
python scripts\build_dataset.py
```

Outputs:
- `data/generated/exhaust_dataset.json`
- `data/generated/dataset_stats.json`

Verified-only output:

```powershell
python scripts\build_dataset.py --verified-only
```

## 5) Validate size and distribution

Check stats:

```powershell
Get-Content data\generated\dataset_stats.json
```

Quick query examples:

```powershell
python scripts\query_dataset.py --make Ducati --limit 15
python scripts\query_dataset.py --status verified --limit 15
```

## 6) Run app locally

```powershell
python -m http.server 8000
```

Open:

`http://localhost:8000/`

## Maintenance Cadence

- Weekly: `pull_sources.py` + `refresh_data.py`.
- Monthly: add verified rows and rerun `build_dataset.py`.
- Before major release: run with `--verified-only` and review result counts.

## Quality Guardrails

- Keep unknown data as null/blank.
- Do not mark fitment as verified without a direct source URL.
- Preserve generation-level year boundaries to avoid mismatched exhaust recommendations.
