# Architecture

This project builds an end-to-end **Decision Intelligence pipeline** from raw retail transactions to:
1) validated KPIs (Excel-style business logic),
2) a PostgreSQL analytics layer (SQL views),
3) customer modeling (RFM segmentation, CLV, churn risk),
4) executive-ready dashboards in Excel and Power BI.

The emphasis is on **traceability**: every metric and model feature is derived from cleaned transactions and reproducible SQL/Python steps.

---

## Components

### 1) Raw Data
- Source: Online Retail II dataset (two Excel sheets: 2009–2010 and 2010–2011)
- Core fields:
  - `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`

### 2) Cleaning and Validation (Python)
Scripts standardize and validate the dataset before analytics and modeling:
- remove cancelled invoices (invoice IDs starting with `C`)
- remove invalid quantities and prices (must be > 0)
- drop rows with missing customer IDs
- parse timestamps into consistent datetime format
- drop exact duplicates after combining sheets

Validation checks confirm:
- zero cancelled invoices after cleaning
- no non-positive quantities or prices
- no missing customer IDs
- all timestamps parse successfully

Outputs:
- a committed cleaned sample for reproducibility
- KPI-ready datasets

### 3) KPI Engine (Python → CSV → Excel)
Python generates KPI tables:
- `kpis_monthly.csv` (month-level KPIs)
- `kpis_monthly_country.csv` (month-by-country KPIs)

KPIs include:
- Revenue, Orders, Active Customers, AOV, Units Sold
- Month-over-month (MoM) changes

Excel consumes these outputs to build a spreadsheet-first reporting layer:
- KPI tiles, pivots, slicers, trends, and country breakdowns
- formulas for MoM and prior-period comparisons

### 4) Database System of Record (PostgreSQL)
Cleaned transactions are loaded into PostgreSQL for scalable analytics.
- schema: `analytics`
- table: `analytics.transactions`

PostgreSQL enables:
- reproducible feature engineering
- reusable SQL views for BI tools (Power BI)
- centralized modeling datasets

### 5) Analytics Layer (SQL Views)
SQL views compute:
- customer RFM features (`analytics.rfm`)
- RFM cluster assignments (`analytics.rfm_segments`)
- monthly KPIs (`analytics.v_kpi_monthly`)
- time-aware customer-month features for churn modeling
- decision tables combining churn + CLV (`analytics.v_customer_decisions`)
- aggregated revenue-at-risk metrics (`analytics.v_revenue_at_risk`)

Key SQL techniques:
- CTEs, joins, aggregations, and window functions (e.g., `NTILE` for deciles)

### 6) Modeling Layer (Python)
Models operate on SQL-produced features:

**Unsupervised (Segmentation)**
- K-Means clustering on RFM features (k=3)

**Probabilistic CLV**
- BG/NBD for purchase frequency
- Gamma-Gamma for monetary value
- output: 90-day CLV per customer (`analytics.clv_90d`)

**Churn Risk (Supervised ML)**
- XGBoost classifier predicting “will buy in next 30 days”
- time split for train/test
- class imbalance handled using `scale_pos_weight`
- explainability using SHAP
- outputs: churn scores + SHAP importance

### 7) BI Layer (Power BI)
Power BI connects directly to PostgreSQL views and surfaces:
- Executive overview KPIs (risk rate, revenue at risk, total CLV)
- Segmentation and value distribution
- High-risk customer action list
- Explainability (SHAP drivers)

---

## Data Flow

1. Raw Excel sheets (Online Retail II)
2. Python cleaning + validation
3. KPI computation → CSV outputs
4. Excel dashboard (Phase 0 reporting)
5. Load cleaned transactions into PostgreSQL
6. SQL analytics views (features + decision tables)
7. Python modeling (RFM, CLV, churn + SHAP)
8. Power BI dashboard (decision intelligence outputs)

---

## Key Outputs

- Cleaned transaction sample + KPI CSVs in `data/processed/`
- Excel dashboard in `excel/`
- PostgreSQL analytics views and decision tables (SQL reproducibility)
- ML outputs: RFM segments, CLV, churn scores, SHAP importance
- Power BI dashboard screenshots in `assets/PowerBI_Dashboard/`
