from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()                                                   #envファイルの読みこみ

DATABASE_URL = os.getenv("DATABASE_URL")                        #URLの取得
if DATABASE_URL is None:                                        #DATABASE_URLの読み込み失敗用
    raise RuntimeError(".envにDATABASE_URLが設定されていません")

engine = create_engine(DATABASE_URL)                            #それぞれの値格納
Session = sessionmaker(bind=engine)
Base = declarative_base()