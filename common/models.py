from sqlalchemy import Column, String, Date, Float, BigInteger, ForeignKey, Boolean
from common.db import Base


class Symbol(Base):                                                           #テーブル設計_Symbol
    __tablename__ = "symbols"
    code = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)


class DailyPrice(Base):                                                       #モデル設計_DailyPrice
    __tablename__ = "daily_prices"
    code = Column(String, ForeignKey("symbols.code"), primary_key=True)
    date = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

