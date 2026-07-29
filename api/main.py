from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession
from common.db import get_db
from common.models import Symbol, DailyPrice
from api.schemas import SymbolOut, DailyPriceOut
from datetime import date
from common.log import configure_logging
import logging


logger = logging.getLogger("api.main")

configure_logging()
logger.info("API を起動しました")

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
    if code is not None:
        symbol_stmt = select(Symbol).where(Symbol.code == code, Symbol.is_active == True)
        symbol = db.execute(symbol_stmt).scalars().first()
        if symbol is None:
            logger.warning("存在しない銘柄が指定されました: %s", code)
            raise HTTPException(status_code=404, detail=f"銘柄 {code} は存在しません")
    
    stmt = select(DailyPrice)

    if code is not None:
        stmt = stmt.where(DailyPrice.code == code)
    if start is not None:
        stmt = stmt.where(DailyPrice.date >= start)
    if end is not None:
        stmt = stmt.where(DailyPrice.date <= end)

    stmt = stmt.order_by(DailyPrice.code, DailyPrice.date)
    return db.execute(stmt).scalars().all()

@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("未処理のエラー: %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )