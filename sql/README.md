# SQL Analytics Layer (PostgreSQL)

This folder contains the **SQL-first analytics layer** used to transform raw Online Retail II transactions into reusable, dashboard-ready outputs. The goal is to keep business logic **centralized in PostgreSQL** (not scattered across notebooks or dashboards), so the same definitions power Excel checks, Python modeling, and Power BI visuals consistently.

The scripts are ordered to be run top-to-bottom. `00_setup.sql` prepares the database structure (schemas and core tables). `01_rfm.sql` builds customer-level **RFM features** and segmentation inputs used for clustering and downstream analysis. `02_kpi_monthly.sql` generates **monthly KPI views** (revenue, orders, active customers, AOV, and related aggregates) that feed the reporting layer.

Finally, `03_customer_decisions.sql` and `04_revenue_at_risk.sql` produce the **decision intelligence outputs** by combining churn risk scores and 90-day CLV into a unified customer decision view and an executive metric for **revenue at risk**. Together, these scripts create the same SQL objects used by Power BI and the ML pipeline, ensuring a traceable path from raw transactions to actionable customer decisions.

