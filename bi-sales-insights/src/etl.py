"""Extract -> Transform -> Load: raw CSV to cleaned SQLite table."""
import sqlite3
import pandas as pd

DB_PATH = "data/sales.db"


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="order_id").copy()
    df["region"] = df["region"].str.strip().str.title().fillna("Unknown")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df = df[df["quantity"] > 0].copy()
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df.reset_index(drop=True)


def load(df: pd.DataFrame, db_path: str = DB_PATH) -> None:
    with sqlite3.connect(db_path) as con:
        df.assign(order_date=df["order_date"].dt.strftime("%Y-%m-%d")).to_sql(
            "sales", con, if_exists="replace", index=False
        )


def run(raw_path: str = "data/raw_sales.csv", db_path: str = DB_PATH) -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    cleaned = clean(raw)
    load(cleaned, db_path)
    print(f"Raw rows: {len(raw)} | Clean rows: {len(cleaned)} -> {db_path}")
    return cleaned


if __name__ == "__main__":
    run()
