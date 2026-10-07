"""Generate a messy synthetic sales dataset (replace with your own CSV if you like)."""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
REGIONS = ["Hyderabad", "Chennai", "Bengaluru", "Mumbai", "Delhi"]
CATEGORIES = {"Electronics": 15000, "Furniture": 8000, "Stationery": 300, "Apparel": 1200}


def generate(n: int = 2000, path: str = "data/raw_sales.csv") -> pd.DataFrame:
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(RNG.integers(0, 365, n), unit="D")
    cats = RNG.choice(list(CATEGORIES), n)
    df = pd.DataFrame({
        "order_id": np.arange(1000, 1000 + n),
        "order_date": dates.strftime("%Y-%m-%d"),
        "region": RNG.choice(REGIONS, n),
        "category": cats,
        "quantity": RNG.integers(1, 10, n),
        "unit_price": [CATEGORIES[c] * RNG.uniform(0.8, 1.2) for c in cats],
    })
    # inject dirt: duplicates, nulls, inconsistent text, invalid values
    df.loc[RNG.choice(n, 40, replace=False), "region"] = None
    df.loc[RNG.choice(n, 30, replace=False), "region"] = "  hyderabad "
    df.loc[RNG.choice(n, 25, replace=False), "quantity"] = -1
    df = pd.concat([df, df.sample(20, random_state=1)], ignore_index=True)
    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    generate()
    print("Wrote data/raw_sales.csv")
