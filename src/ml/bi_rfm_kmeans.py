import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DB_URL = os.getenv("DB_URL")  # example: postgresql+psycopg2://user:pass@localhost:5432/retail
engine = create_engine(DB_URL)

df = pd.read_sql("SELECT customer_id, recency_days, frequency, monetary FROM analytics.rfm", engine)

X = df[["recency_days", "frequency", "monetary"]].copy()

# log-transform monetary/frequency (common for retail skew)
# X["frequency"] = (X["frequency"] + 1).apply(lambda x: float(pd.np.log(x)))
X["frequency"] = np.log(X["frequency"] + 1)
# X["monetary"] = (X["monetary"] + 1).apply(lambda x: float(pd.np.log(x)))
X["monetary"] = np.log(X["monetary"] + 1)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

best_k, best_score = None, -1
for k in [3, 4, 5, 6]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    if score > best_score:
        best_k, best_score = k, score

km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df["rfm_cluster"] = km.fit_predict(X_scaled)

# label clusters using business logic: high monetary+freq, low recency = best
cluster_profile = df.groupby("rfm_cluster")[["recency_days","frequency","monetary"]].mean().reset_index()
cluster_profile["rank_score"] = (-cluster_profile["recency_days"]) + cluster_profile["frequency"] + cluster_profile["monetary"]
cluster_profile = cluster_profile.sort_values("rank_score", ascending=False)

labels_map = {}
label_names = ["Champions", "Loyalists", "At Risk", "Hibernating", "New", "Needs Attention"]
for i, row in enumerate(cluster_profile.itertuples(index=False)):
    labels_map[row.rfm_cluster] = label_names[i] if i < len(label_names) else f"Segment_{i}"

df["rfm_segment"] = df["rfm_cluster"].map(labels_map)

out = df[["customer_id","rfm_cluster","rfm_segment"]].copy()
out["silhouette"] = best_score
out["k"] = best_k

out.to_sql("rfm_segments", engine, schema="analytics", if_exists="replace", index=False)

print(f"Saved analytics.rfm_segments (k={best_k}, silhouette={best_score:.3f})")
