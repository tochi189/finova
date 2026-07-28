from datetime import date
from pydantic import BaseModel, ConfigDict

class SymbolOut(BaseModel):
    code: str
    name: str
    sector: str

    model_config = ConfigDict(from_attributes=True)

class DailyPriceOut(BaseModel):
    code: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    model_config = ConfigDict(from_attributes=True)