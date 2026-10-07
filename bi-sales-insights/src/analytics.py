"""KPI calculations using SQL + Pandas."""
import sqlite3
import pandas as pd
from src.etl import DB_PATH


def _query(sql: str, db_path: str = DB_PATH) -> pd.DataFrame:
    with sqlite3.connect(db_path) as con:
        return pd.read_sql_query(sql, con)


def summary(db_path: str = DB_PATH) -> dict:
    df = _query(
        "SELECT COUNT(*) AS orders, SUM(revenue) AS revenue, AVG(revenue) AS aov FROM sales",
        db_path,
    )
    r = df.iloc[0]
    return {"orders": int(r.orders), "revenue": round(r.revenue, 2), "avg_order_value": round(r.aov, 2)}


def revenue_by(column: str, db_path: str = DB_PATH) -> list[dict]:
    if column not in {"region", "category"}:
        raise ValueError("dimension must be 'region' or 'category'")
    df = _query(
        f"SELECT {column}, ROUND(SUM(revenue),2) AS revenue FROM sales "
        f"GROUP BY {column} ORDER BY revenue DESC",
        db_path,
    )
    return df.to_dict("records")


def monthly_trend(db_path: str = DB_PATH) -> list[dict]:
    df = _query("SELECT month, ROUND(SUM(revenue),2) AS revenue FROM sales GROUP BY month ORDER BY month", db_path)
    df["mom_growth_pct"] = (df["revenue"].pct_change() * 100).round(2)
    return df.fillna(0).to_dict("records")
