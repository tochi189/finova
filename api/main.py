from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from common.db import get_db
from common.models import Symbol
from api.schemas import SymbolOut

app = FastAPI(
    title="finova2 API",
    description="株価データを提供する API",
    version="0.1.0",
)

@app.get("/symbols", response_model=list[SymbolOut])
def get_symbols(db:DbSession = Depends(get_db)):
    stmt = select(Symbol).where(Symbol.is_active == True)
    return db.execute(stmt).scalars().all()