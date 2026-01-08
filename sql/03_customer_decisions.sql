CREATE OR REPLACE VIEW analytics.v_customer_decisions AS
WITH latest_scores AS (
  SELECT DISTINCT ON (customer_id)
    customer_id,
    month,
    churn_risk_score
  FROM analytics.churn_scores
  ORDER BY customer_id, month DESC
),
scored AS (
  SELECT
    customer_id,
    churn_risk_score,
    NTILE(10) OVER (ORDER BY churn_risk_score DESC) AS risk_decile,
    CASE
      WHEN NTILE(10) OVER (ORDER BY churn_risk_score DESC) = 1 THEN TRUE
      ELSE FALSE
    END AS high_risk
  FROM latest_scores
)
SELECT
  s.customer_id,
  s.churn_risk_score,
  s.risk_decile,
  s.high_risk,
  seg.rfm_segment,
  clv.clv_90d,
  CASE WHEN s.high_risk THEN clv.clv_90d ELSE 0 END AS revenue_at_risk_90d_per_customer
FROM scored s
LEFT JOIN analytics.rfm_segments seg
  ON s.customer_id::bigint = seg.customer_id::bigint
LEFT JOIN analytics.clv_90d clv
  ON s.customer_id::bigint = clv.customer_id::bigint;
