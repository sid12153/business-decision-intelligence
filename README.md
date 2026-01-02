![Analytics](https://img.shields.io/badge/Domain-Business%20Analytics-blue)
![ML](https://img.shields.io/badge/ML-Customer%20Modeling-orange)
![Clustering](https://img.shields.io/badge/Unsupervised-RFM%20Clustering-purple)
![Probabilistic](https://img.shields.io/badge/Modeling-BG%2FNBD%20%7C%20Gamma--Gamma-green)
![Explainability](https://img.shields.io/badge/Explainability-SHAP-red)
![Decision Intelligence](https://img.shields.io/badge/Outcome-Revenue%20at%20Risk-black)

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

## Excel Reporting Layer - Dashboard

A final Excel-based dashboard was built on top of the validated KPI outputs to support business review and decision-making.

The dashboard includes:
- KPI cards for revenue, orders, active customers, and average order value
- Month-over-month comparisons using date-based formulas
- Trend analysis for revenue, orders, and customer activity
- Country-level revenue breakdown with explicit handling of skewed distributions

All metrics were validated against the Python-generated KPIs to ensure consistency between data processing and reporting layers.

## Executive Summary

This project develops a decision intelligence reporting layer using transactional retail data to analyze revenue performance, customer activity, and order behavior over time.

Monthly analysis reveals clear seasonality, with revenue consistently peaking during September to November and declining in December, driven primarily by reduced order volume rather than changes in average order value. Revenue is highly concentrated in the United Kingdom, while several non-UK markets contribute smaller but stable revenue streams, highlighting both geographic dependence and diversification opportunities.

Average Order Value trends upward across the observed period, indicating improved per-order monetization even during periods of fluctuating customer activity. All key metrics were validated through reconciliation checks between raw data, Python-based KPI generation, and Excel-based calculations to ensure analytical accuracy and transparency.

The final output includes a validated Excel dashboard designed for business review, emphasizing clarity, correctness, and real-world reporting practices rather than interactivity or visualization complexity.
