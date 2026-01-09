# Power BI Dashboard (Business Decision Intelligence)

This dashboard is the final “decision layer” of the project. It connects directly to the PostgreSQL analytics schema and turns customer modeling outputs (RFM segments, CLV, churn risk, and SHAP drivers) into actionable business views.

**File:** `assets/PowerBI_Dashboard/Business_Decision_Intelligence.pbix`  
**Primary source:** PostgreSQL (analytics schema) via `127.0.0.1:5433`

---

## Data Model (Power BI Sources)

Power BI loads these main objects from PostgreSQL:

- `analytics.v_customer_decisions`  
  Unified decision table with customer-level churn risk, risk decile, high-risk flag, RFM segment, CLV (90d), and revenue-at-risk per customer.

- `analytics.v_kpi_monthly`  
  Monthly KPIs: revenue, orders, active customers, AOV, and revenue per customer.

- `analytics.shap_importance`  
  Global feature importance table used for churn explainability.

Supporting tables (used upstream to build the views):

- `analytics.rfm`
- `analytics.rfm_segments`
- `analytics.clv_90d`
- `analytics.churn_scores`

---

## Page 1 — Executive Overview

Purpose: Provide an executive snapshot of customer value, churn exposure, and financial impact.

Key visuals:
- KPI cards:
  - Customers
  - High-risk customers
  - High-risk rate
  - Total CLV (90 days)
  - Revenue at risk (90 days)
- Segment view:
  - Revenue at risk by RFM segment

Screenshot:
- `assets/PowerBI_Dashboard/ExecutiveOverview_Page_1.jpg`

Notes:
- “High risk” is defined using a threshold on churn risk score (risk decile logic from the decision view).
- Revenue at risk is computed by summing CLV for customers flagged as high risk.

---

## Page 2 — Segmentation (RFM)

Purpose: Explain customer segments and how value (CLV) concentrates across segments.

Key visuals:
- Customer count by RFM segment
- Average CLV by RFM segment
- Revenue at risk by RFM segment
- Summary table:
  - Segment, customers, avg CLV, revenue at risk

Screenshot:
- `assets/PowerBI_Dashboard/Segmentation_Page_2.jpg`

Notes:
- Segments originate from K-Means clustering over RFM features (recency, frequency, monetary).
- This page answers: “Which segments are most valuable?” and “Where is the risk concentrated?”

---

## Page 3 — High-Risk Customers (Action List)

Purpose: Provide an operational “call list” for retention or intervention.

Key visuals:
- Customer table sorted by churn risk:
  - customer_id
  - churn_risk_score
  - risk_decile
  - high_risk flag
  - rfm_segment
  - clv_90d
  - revenue_at_risk_90d_per_customer
- Filters:
  - High risk only (TRUE)
  - Optional: segment filter

Screenshot:
- `assets/PowerBI_Dashboard/High_Risk_Customer_Page_3.jpg`

Notes:
- This page translates model outputs into direct actions:
  - who to contact first
  - how much value is at stake per customer (CLV proxy)

---

## Page 4 — Explainability (SHAP)

Purpose: Explain what drives churn risk globally, so decisions are interpretable.

Key visuals:
- Bar chart of mean absolute SHAP values:
  - orders
  - monetary
  - recency_days

Screenshot:
- `assets/PowerBI_Dashboard/SHAP_Page_4.jpg`

Notes:
- SHAP values are computed from the XGBoost churn model and written back into PostgreSQL.
- This page answers: “Why is churn risk increasing?” with model-grounded drivers.

---

## How to Open / Share

- Open the dashboard locally using:
  - `assets/PowerBI_Dashboard/Business_Decision_Intelligence.pbix`

- Screenshots for quick review:
  - `assets/PowerBI_Dashboard/ExecutiveOverview_Page_1.jpg`
  - `assets/PowerBI_Dashboard/Segmentation_Page_2.jpg`
  - `assets/PowerBI_Dashboard/High_Risk_Customer_Page_3.jpg`
  - `assets/PowerBI_Dashboard/SHAP_Page_4.jpg`

---

## What This Dashboard Demonstrates

- Spreadsheet-style KPIs upgraded into a database-backed analytics layer
- Customer segmentation (RFM clustering) + probabilistic value modeling (CLV)
- Supervised churn modeling with explainability (XGBoost + SHAP)
- Decision intelligence translation: churn risk → revenue at risk
- Executive-ready visuals plus an operational action list
