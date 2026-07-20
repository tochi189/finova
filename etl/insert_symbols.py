from common.db import Session, engine, Base
from sqlalchemy import Column, String
from pathlib import Path
import csv

class Symbol(Base):                                 #テーブル設計
    __tablename__ = "symbols"
    code = Column(String, primary_key=True)
    name = Column(String)
    sector = Column(String)

Base.metadata.create_all(engine)                     #新規でテーブル作成

csv_path = Path(__file__).parent.parent / "data" / "symbols.csv"
symbols = []
with open(csv_path, encoding="utf-8-sig", newline="") as f:           #symbols.csvの読み込み
    reader = csv.DictReader(f)
    for row in reader:
        symbols.append(Symbol(code=row["code"], name=row["name"], sector=row["sector"]))





session = Session()
try:
    session.add_all(symbols)
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()