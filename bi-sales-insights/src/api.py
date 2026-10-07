"""FastAPI service exposing KPIs. Run: uvicorn src.api:app --reload"""
from fastapi import FastAPI, HTTPException
from src import analytics

app = FastAPI(title="BI Sales Insights API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "BI Sales Insights API. See /docs"}


@app.get("/kpis")
def kpis():
    return analytics.summary()


@app.get("/revenue/{dimension}")
def revenue(dimension: str):
    try:
        return analytics.revenue_by(dimension)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/trend")
def trend():
    return analytics.monthly_trend()
