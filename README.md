# Business Decision Intelligence for KPI Analysis and Forecasting
Business decisions are often driven by metrics such as revenue, growth, retention, and customer behavior. In practice, these metrics are usually computed in spreadsheets, explored through ad-hoc analysis, and explained manually in reports or presentations.

This project focuses on building a structured decision intelligence workflow around these common business analyses. Using real transactional data, the system computes core KPIs, tracks how they change over time, and applies statistical and machine learning models to identify trends and potential risks.

The emphasis of the project is on clarity and interpretability. KPI definitions follow spreadsheet-style logic, model outputs are explainable, and results are presented in formats that would be familiar to business and analytics teams, including Excel-based reports and concise written summaries.

## Data Processing

The Online Retail II dataset was cleaned and prepared using a reproducible Python pipeline.

### Cleaning steps
The following data quality rules were applied prior to any analysis:
- Removed cancelled invoices (invoice numbers starting with `"C"`)
- Removed rows with non-positive quantities or prices
- Removed rows with missing customer identifiers
- Parsed invoice timestamps into a consistent datetime format
- Dropped exact duplicate rows after combining multiple data sheets

All cleaning decisions are documented in `cleaning_rules.md`.

## Processed Data Files

Due to file size constraints, the full cleaned dataset is not tracked in this repository.

The following files are provided:

- `data/processed/transactions_clean_sample.csv`  
  A 100,000-row sample of the fully cleaned dataset, included for inspection and reproducibility.

To generate the full cleaned dataset locally:
1. Download the Online Retail II dataset from the UCI repository
2. Place the raw Excel file at `data/raw/online_retail_II.xlsx`
3. Run:
   ```bash
   python src/data/clean_transactions.py
This will create:
data/processed/transactions_clean.csv (full cleaned dataset, generated locally)

## KPI Engine

A reproducible KPI engine was built in Python to compute monthly business performance metrics from cleaned transactional data.

The pipeline generates:
- `kpis_monthly.csv`: overall monthly business KPIs
- `kpis_monthly_country.csv`: country-level monthly KPI breakdowns

KPIs include revenue, orders, active customers, units sold, average order value (AOV), and month-over-month growth metrics.
All KPI definitions and formulas are documented in `kpi_definitions.md`.

## KPI Validation

Computed KPIs were validated using multiple consistency checks:
- Logical checks ensuring Orders ≥ Active Customers for all months
- Month-over-month growth sanity checks across the time series
- Reconciliation of country-level revenue against overall business revenue

Country-level aggregations reconcile exactly with overall metrics, confirming aggregation correctness.

## Excel Reporting Layer

An Excel-based reporting layer was built on top of the processed KPI outputs to support business review and validation.

The dashboard includes:
- KPI cards for latest month revenue, orders, active customers, and AOV
- Monthly trend analysis using pivot charts with dual-axis scaling
- Country-level revenue comparison with explicit handling of skewed distributions
- Formula-based validation checks (AOV recomputation and revenue reconciliation)

The Excel layer emphasizes transparency and correctness rather than interactivity, mirroring real-world BI reporting practices.
