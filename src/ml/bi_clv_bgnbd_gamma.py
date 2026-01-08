import os
import pandas as pd
from sqlalchemy import create_engine
from lifetimes.utils import summary_data_from_transaction_data
from lifetimes import BetaGeoFitter, GammaGammaFitter
import matplotlib.pyplot as plt

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

tx = pd.read_sql("""
SELECT customer_id, invoice_datetime, revenue
FROM analytics.v_txn_purchases
""", engine)

tx["invoice_datetime"] = pd.to_datetime(tx["invoice_datetime"])
tx["customer_id"] = tx["customer_id"].astype(str)

# RFM summary for lifetimes
summary = summary_data_from_transaction_data(
    tx,
    customer_id_col="customer_id",
    datetime_col="invoice_datetime",
    monetary_value_col="revenue",
    observation_period_end=tx["invoice_datetime"].max()
)

# Fit BG/NBD
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(summary["frequency"], summary["recency"], summary["T"])

# Fit Gamma-Gamma (requires monetary_value > 0)
summary_gg = summary[summary["monetary_value"] > 0].copy()
ggf = GammaGammaFitter(penalizer_coef=0.001)
ggf.fit(summary_gg["frequency"], summary_gg["monetary_value"])

# Predict next 90 days
t_days = 90
summary["pred_purchases_90d"] = bgf.conditional_expected_number_of_purchases_up_to_time(
    t_days, summary["frequency"], summary["recency"], summary["T"]
)

summary["exp_avg_value"] = ggf.conditional_expected_average_profit(
    summary_gg["frequency"], summary_gg["monetary_value"]
).reindex(summary.index)

summary["clv_90d"] = summary["pred_purchases_90d"] * summary["exp_avg_value"]

out = summary.reset_index().rename(columns={"index": "customer_id"})
out = out[["customer_id","frequency","recency","T","monetary_value","pred_purchases_90d","exp_avg_value","clv_90d"]]

out.to_sql("clv_90d", engine, schema="analytics", if_exists="replace", index=False)

print("Saved analytics.clv_90d")
print(out.sort_values("clv_90d", ascending=False).head(10))
