from common.db import Session, engine, Base
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert             #upsert用インポート
from pathlib import Path
from common.models import Symbol, DailyPrice
from common.log import configure_logging
import csv
import logging



#ログ設定
logger = logging.getLogger("etl.upsert_symbols")

#処理の関数化
def sync_symbols() -> None:
    #新規でテーブル作成
    Base.metadata.create_all(engine)                     

    #symbols.csvの読み込み
    csv_path = Path(__file__).parent.parent / "data" / "symbols.csv"
    with open(csv_path, encoding="utf-8-sig", newline="") as f:           
        reader = csv.DictReader(f)
        rows = list(reader)
        logger.info("csv読み込み完了：%d件", len(rows))
        
        #csvにない銘柄を非アクティブ化
        csv_codes = [row["code"]for row in rows]
        deactivate_stmt = (
            update(Symbol)
            .where(Symbol.code.notin_(csv_codes))
            .values(is_active=False)
        )

        #アクティブになっているものをinsert、update
        for row in rows:
            row["is_active"] = True
        stmt = insert(Symbol).values(rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["code"],
            set_= {
                "name":stmt.excluded.name,
                "sector":stmt.excluded.sector,
                "is_active": stmt.excluded.is_active,
            } ,
        
        )
            

    session = Session()
    try:
        session.execute(deactivate_stmt)
        session.execute(stmt)
        session.commit()
        logger.info("symbols同期完了：%d件", len(rows))
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    configure_logging()
    logger.info("symbols マスタ同期開始")
    sync_symbols()