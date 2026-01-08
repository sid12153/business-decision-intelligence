# import os
# import pandas as pd
# import numpy as np
# from sqlalchemy import create_engine
# from xgboost import XGBClassifier
# from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
# import shap

# DB_URL = os.getenv("DB_URL")
# engine = create_engine(DB_URL)

# df = pd.read_sql("""
# SELECT customer_id, month, orders, monetary, recency_days, will_buy_next_30d
# FROM analytics.customer_monthly_features
# WHERE recency_days IS NOT NULL
# """, engine)

# df["month"] = pd.to_datetime(df["month"])
# df = df.sort_values("month")

# # time split: last 3 months = test (adjust if needed)
# cutoff = df["month"].max() - pd.offsets.MonthBegin(3)

# train = df[df["month"] < cutoff].copy()
# test  = df[df["month"] >= cutoff].copy()

# features = ["orders", "monetary", "recency_days"]
# X_train, y_train = train[features], train["will_buy_next_30d"]
# X_test, y_test   = test[features], test["will_buy_next_30d"]

# model = XGBClassifier(
#     n_estimators=300,
#     max_depth=4,
#     learning_rate=0.05,
#     subsample=0.9,
#     colsample_bytree=0.9,
#     random_state=42,
#     eval_metric="logloss"
# )
# model.fit(X_train, y_train)

# proba = model.predict_proba(X_test)[:, 1]
# pred = (proba >= 0.5).astype(int)

# auc = roc_auc_score(y_test, proba)
# p, r, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", zero_division=0)

# print(f"AUC={auc:.3f}  Precision={p:.3f}  Recall={r:.3f}  F1={f1:.3f}")

# # Save predictions back for dashboard
# out = test[["customer_id","month"]].copy()
# out["churn_risk_score"] = 1 - proba  # higher means more likely to churn (not buy)
# out["will_buy_next_30d"] = y_test.values
# out.to_sql("churn_scores", engine, schema="analytics", if_exists="replace", index=False)

# # SHAP explainability
# explainer = shap.TreeExplainer(model)
# shap_values = explainer.shap_values(X_test)

# # Global importance (mean abs SHAP)
# imp = pd.DataFrame({
#     "feature": features,
#     "mean_abs_shap": np.abs(shap_values).mean(axis=0)
# }).sort_values("mean_abs_shap", ascending=False)

# imp.to_sql("shap_importance", engine, schema="analytics", if_exists="replace", index=False)
# print("Saved analytics.churn_scores and analytics.shap_importance")
# print(imp)
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
import shap

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

df = pd.read_sql("""
SELECT customer_id, month, orders, monetary, recency_days, will_buy_next_30d
FROM analytics.customer_monthly_features
WHERE recency_days IS NOT NULL
""", engine)

df["month"] = pd.to_datetime(df["month"])
df = df.sort_values("month")

# time split: last 3 months = test (adjust if needed)
cutoff = df["month"].max() - pd.offsets.MonthBegin(3)

train = df[df["month"] < cutoff].copy()
test  = df[df["month"] >= cutoff].copy()

features = ["orders", "monetary", "recency_days"]
X_train, y_train = train[features], train["will_buy_next_30d"]
X_test, y_test   = test[features], test["will_buy_next_30d"]

# ✅ class imbalance handling (compute from TRAIN only)
pos = (y_train == 1).sum()
neg = (y_train == 0).sum()
scale_pos_weight = (neg / pos) if pos > 0 else 1.0

model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,  # ✅ add here
)
model.fit(X_train, y_train)

proba = model.predict_proba(X_test)[:, 1]
# pred = (proba >= 0.5).astype(int)
threshold = 0.4
pred = (proba >= threshold).astype(int)


auc = roc_auc_score(y_test, proba)
p, r, f1, _ = precision_recall_fscore_support(y_test, pred, average="binary", zero_division=0)

print(f"scale_pos_weight={scale_pos_weight:.3f}")
print(f"AUC={auc:.3f}  Precision={p:.3f}  Recall={r:.3f}  F1={f1:.3f}")

# Save predictions back for dashboard
out = test[["customer_id","month"]].copy()
out["churn_risk_score"] = 1 - proba  # higher means more likely to churn (not buy)
out["will_buy_next_30d"] = y_test.values
out.to_sql("churn_scores", engine, schema="analytics", if_exists="replace", index=False)

# SHAP explainability
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Global importance (mean abs SHAP)
imp = pd.DataFrame({
    "feature": features,
    "mean_abs_shap": np.abs(shap_values).mean(axis=0)
}).sort_values("mean_abs_shap", ascending=False)

imp.to_sql("shap_importance", engine, schema="analytics", if_exists="replace", index=False)
print("Saved analytics.churn_scores and analytics.shap_importance")
print(imp)
