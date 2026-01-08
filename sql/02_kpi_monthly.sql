CREATE OR REPLACE VIEW analytics.v_kpi_monthly AS
WITH base AS (
  SELECT
    invoice_no,
    customer_id::bigint AS customer_id,
    invoice_datetime::timestamp AS invoice_datetime,
    revenue::numeric AS revenue
  FROM analytics.transactions
  WHERE customer_id IS NOT NULL
),
m AS (
  SELECT
    DATE_TRUNC('month', invoice_datetime)::date AS month,
    SUM(revenue) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS active_customers
  FROM base
  GROUP BY 1
)
SELECT
  month,
  revenue,
  orders,
  active_customers,
  CASE WHEN orders = 0 THEN NULL ELSE revenue / orders END AS aov,
  CASE WHEN active_customers = 0 THEN NULL ELSE revenue / active_customers END AS revenue_per_customer
FROM m
ORDER BY month;
