import logging
from pathlib import Path

_configured = False

def configure_logging() -> None:
    """ロガーの初期設定、複数回呼ばれても1回だけ設定する"""
    global _configured
    if _configured:
        return
    _configured = True

    #ログファイルの置き場所
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)                       #フォルダがあってもエラーにしない
    log_file = log_dir / "etl.log"

    #ルートロガーを取得（全ファイル共通の親）
    logger = logging.getLogger()       #INFO以上を出力
    logger.setLevel(logging.INFO)

    #フォーマット
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    #コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #ファイル出力(追記)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

