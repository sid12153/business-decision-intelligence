CREATE OR REPLACE VIEW analytics.v_revenue_at_risk AS
SELECT
  SUM(revenue_at_risk_90d_per_customer) AS revenue_at_risk_90d,
  COUNT(*) FILTER (WHERE high_risk) AS high_risk_customers
FROM analytics.v_customer_decisions;
