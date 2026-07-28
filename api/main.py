from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession
from common.db import get_db
from common.models import Symbol, DailyPrice
from api.schemas import SymbolOut, DailyPriceOut
from datetime import date

app = FastAPI(
    title="finova2 API",
    description="株価データを提供する API",
    version="0.1.0",
)

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/symbols", response_model=list[SymbolOut])
def get_symbols(db:DbSession = Depends(get_db)):
    stmt = select(Symbol).where(Symbol.is_active == True)
    return db.execute(stmt).scalars().all()

@app.get("/prices", response_model=list[DailyPriceOut])
def get_prices(
    code: str | None = None,
    start: date | None = None,
    end: date | None = None,
    db: DbSession =Depends(get_db),
):
    stmt = select(DailyPrice)

    if code is not None:
        stmt = stmt.where(DailyPrice.code == code)
    if start is not None:
        stmt = stmt.where(DailyPrice.date >= start)
    if end is not None:
        stmt = stmt.where(DailyPrice.date <= end)

    stmt = stmt.order_by(DailyPrice.code, DailyPrice.date)
    return db.execute(stmt).scalars().all()