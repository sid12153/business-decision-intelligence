CREATE OR REPLACE VIEW analytics.rfm AS
WITH base AS (
  SELECT
    customer_id::bigint AS customer_id,
    invoice_no,
    invoice_datetime::timestamp AS invoice_datetime,
    revenue::numeric AS revenue
  FROM analytics.transactions
  WHERE customer_id IS NOT NULL
),
last_date AS (
  SELECT MAX(invoice_datetime) AS max_dt FROM base
),
by_customer AS (
  SELECT
    b.customer_id,
    (SELECT max_dt FROM last_date) - MAX(b.invoice_datetime) AS recency_interval,
    COUNT(DISTINCT b.invoice_no) AS frequency,
    SUM(b.revenue) AS monetary
  FROM base b
  GROUP BY 1
)
SELECT
  customer_id,
  EXTRACT(DAY FROM recency_interval) AS recency_days,
  frequency,
  monetary
FROM by_customer;
