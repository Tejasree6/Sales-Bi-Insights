import pandas as pd
from src.etl import clean


def test_clean_removes_dupes_and_bad_rows():
    raw = pd.DataFrame({
        "order_id": [1, 1, 2, 3],
        "order_date": ["2025-01-01"] * 4,
        "region": [" delhi ", " delhi ", None, "Mumbai"],
        "category": ["A"] * 4,
        "quantity": [2, 2, 3, -1],
        "unit_price": [10.0] * 4,
    })
    out = clean(raw)
    assert len(out) == 2
    assert set(out["region"]) == {"Delhi", "Unknown"}
    assert out.loc[0, "revenue"] == 20.0
