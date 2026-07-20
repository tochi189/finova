# finova プロジェクト構成

株価データを収集・保存し、Power BI で可視化する BI システム。

## 全体像

```
yfinance → ETL(Python) → PostgreSQL → FastAPI → Power BI
```

- **ETL**: yfinance で株価データを取得し、整形して DB に保存する
- **DB**: PostgreSQL（finova データベース）。symbols / daily_prices の2テーブル
- **API**: FastAPI。DB のデータを Power BI に渡す窓口
- **可視化**: Power BI。3ページ構成のダッシュボード

## フォルダ構成

```
├── common\             ← 共通部品（DB接続など）
│   ├── __init__.py
│   └── db.py
├── etl\                ← データ収集・投入
│   ├── __init__.py
│   ├── config.py
│   ├── insert_symbols.py
│   └── main.py
├── api\                ← FastAPI
│   ├── __init__.py
│   └── main.py
├── docs\ 
└── requirements.txt
```

## import とパッケージの方針

- 各フォルダに `__init__.py` を置き、正式な Python パッケージとして扱う
- `sys.path.append` は使わない
- モジュール間の参照は `from common.db import ...` の形で書く

## 実行ルール

**実行の起点は常にリポジトリのルート。`-m` 形式で実行する。**

```powershell
# ETL 系
python -m etl.insert_symbols
python -m etl.main

# API 起動
python -m uvicorn api.main:app --reload
```

理由: 実行場所がバラバラだと import の解決が不安定になるため、
起点を1つに固定する。

## DB 接続

- 接続情報（DATABASE_URL）は .env で管理し、common/db.py が読み込む
- ソースコードに接続文字列やパスワードを直接書かない

## セキュリティ

- 認証情報・API キーは環境変数（.env）で管理する
- .env は .gitignore に入れてコミットしない
