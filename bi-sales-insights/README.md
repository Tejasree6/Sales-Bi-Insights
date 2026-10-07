# BI Sales Insights

An end-to-end analytics mini-project: **raw CSV → cleaning (Pandas) → SQLite → KPI queries (SQL) → REST API (FastAPI)**.

## Features
- Data cleaning: duplicates, nulls, inconsistent text, invalid quantities
- Derived metrics: revenue, month, average order value, MoM growth
- SQL aggregations by region, category and month
- FastAPI endpoints with auto-generated docs
- Unit tests with pytest

## Project structure
```
src/
  generate_data.py   # synthetic messy dataset (swap in your own CSV)
  etl.py             # clean + load into SQLite
  analytics.py       # KPI functions
  api.py             # FastAPI app
tests/test_etl.py
run_pipeline.py
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_pipeline.py
uvicorn src.api:app --reload
```
Open http://127.0.0.1:8000/docs

## Endpoints
| Endpoint | Description |
|---|---|
| `GET /kpis` | Orders, total revenue, average order value |
| `GET /revenue/region` | Revenue by region |
| `GET /revenue/category` | Revenue by category |
| `GET /trend` | Monthly revenue with MoM growth % |

## Run tests
```bash
pytest
```

## Ideas to extend
- Plug in a real Indian government open dataset (data.gov.in)
- Connect the SQLite DB to Power BI and build a dashboard on top
- Add a Dockerfile and GitHub Actions CI
