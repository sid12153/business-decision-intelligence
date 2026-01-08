import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

OBJECTS = [
    ("analytics", "rfm"),
    ("analytics", "rfm_segments"),
    ("analytics", "clv_90d"),
    ("analytics", "customer_monthly_features"),          
    ("analytics", "churn_scores"),
    ("analytics", "shap_importance"),
    ("analytics", "v_kpi_monthly"),              # views also ok
    ("analytics", "v_rfm_segment_kpis"),
    ("analytics", "v_high_risk_customers"),
    ("analytics", "v_revenue_at_risk"),
    ("analytics", "v_customer_decisions"),
]

def exists(schema: str, name: str) -> bool:
    q = text("""
        SELECT EXISTS (
          SELECT 1
          FROM information_schema.tables
          WHERE table_schema = :s AND table_name = :n
        )
        OR EXISTS (
          SELECT 1
          FROM information_schema.views
          WHERE table_schema = :s AND table_name = :n
        ) AS ok;
    """)
    with engine.connect() as conn:
        return bool(conn.execute(q, {"s": schema, "n": name}).scalar())

def main():
    for schema, name in OBJECTS:
        if not exists(schema, name):
            print(f"SKIP (missing): {schema}.{name}")
            continue

        query = f'SELECT * FROM "{schema}"."{name}"'
        df = pd.read_sql(query, engine)

        out_path = os.path.join(EXPORT_DIR, f"{name}.csv")
        df.to_csv(out_path, index=False, encoding="utf-8")
        print(f"Saved {schema}.{name} -> {out_path}  (rows={len(df)})")

if __name__ == "__main__":
    main()
