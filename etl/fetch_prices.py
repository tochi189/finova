from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from common.models import Symbol, DailyPrice
from common.db import Session
from pandas import DataFrame
from common.log import configure_logging
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import yfinance as yf
import logging



#ログ設定
logger = logging.getLogger("etl.fetch_prices")

#アクティブの銘柄を取得
def get_target_codes() -> list[str]:
    session = Session()
    try:
        stmt = select(Symbol.code).where(Symbol.is_active == True)
        result = session.execute(stmt)
        codes = [row[0] for row in result]
        logger.info("対象銘柄取得：%d件", len(codes))
        return codes
    finally:
        session.close()


#データ取得失敗時のリトライ処理
@retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING),
)
def _fetch_one(code: str) -> DataFrame:
    """1銘柄分の株価を取得（失敗時は3回リトライ）"""
    ticker = yf.Ticker(code)
    return ticker.history(period="7d")

#銘柄の日付ごとのデータを取得
def ingest(codes: list[str]) -> dict[str, DataFrame]:
    logger.info("株価取得開始：%d銘柄", len(codes))
    result = {}
    for code in codes:
        df= _fetch_one(code)
        result[code] = df
        logger.info("取得完了：%s(%d行)", code, len(df))
    return result


#辞書リストに変換
def transform(raw: dict[str, DataFrame]) ->list[dict]:
    all_rows =[]
    for code, df in raw.items():
        df = df.reset_index()
        df.columns = df.columns.str.lower()
        df["code"] = code
        df["date"] = df["date"].dt.date
        df = df[["code", "date", "open", "high", "low", "close", "volume"]]
        rows = df.to_dict(orient="records")
        all_rows.extend(rows)
    logger.info("整形完了：合計%d件", len(all_rows))
    return all_rows



#daily_pricesに投入
def load(rows: list[dict]) -> None:
    logger.info("DB投入開始：%d件", len(rows))
    stmt = insert(DailyPrice).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["code", "date"],
        set_= {
            "open": stmt.excluded.open,
            "high": stmt.excluded.high,
            "low": stmt.excluded.low,
            "close": stmt.excluded.close,
            "volume": stmt.excluded.volume,
        },
    )

    session = Session()
    try:
        session.execute(stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    



if __name__ == "__main__":
    configure_logging()                              #ログ初期化
    codes = get_target_codes()
    raw = ingest(codes)
    rows = transform(raw)
    load(rows)
    logger.info("ETL完了: %d 件をdaily_pricesに投入", len(rows))   

