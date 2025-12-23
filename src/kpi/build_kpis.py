import pandas as pd
from pathlib import Path


def load_clean_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["InvoiceDate"])


def add_invoice_month(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    return df


def compute_monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df["Revenue"] = df["Quantity"] * df["Price"]

    monthly = (
        df.groupby("InvoiceMonth")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            ActiveCustomers=("Customer ID", "nunique"),
            UnitsSold=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values("InvoiceMonth")
    )

    monthly["AOV"] = monthly["Revenue"] / monthly["Orders"]
    monthly["Revenue_MoM_Growth"] = monthly["Revenue"].pct_change()
    monthly["ActiveCustomers_MoM_Growth"] = monthly["ActiveCustomers"].pct_change()

    return monthly


def compute_monthly_kpis_by_country(df: pd.DataFrame) -> pd.DataFrame:
    df["Revenue"] = df["Quantity"] * df["Price"]

    country_monthly = (
        df.groupby(["InvoiceMonth", "Country"])
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            ActiveCustomers=("Customer ID", "nunique"),
            UnitsSold=("Quantity", "sum"),
        )
        .reset_index()
        .sort_values(["Country", "InvoiceMonth"])
    )

    country_monthly["AOV"] = country_monthly["Revenue"] / country_monthly["Orders"]

    return country_monthly


def main():
    input_path = Path("data/processed/transactions_clean.csv")
    output_dir = Path("data/processed")
    
    df = load_clean_data(input_path)
    df = add_invoice_month(df)

    kpis_monthly = compute_monthly_kpis(df)
    kpis_country = compute_monthly_kpis_by_country(df)

    output_dir.mkdir(parents=True, exist_ok=True)
    kpis_monthly.to_csv(output_dir / "kpis_monthly.csv", index=False)
    kpis_country.to_csv(output_dir / "kpis_monthly_country.csv", index=False)

    print("KPI files generated:")
    print("- kpis_monthly.csv")
    print("- kpis_monthly_country.csv")


if __name__ == "__main__":
    main()

