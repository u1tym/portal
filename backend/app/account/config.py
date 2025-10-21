import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

# アカウント用データベース設定
ACCOUNT_DATABASE_URL = os.getenv("ACCOUNT_DATABASE_URL", "postgresql://puser:ppassword@localhost:5432/portal?client_encoding=utf8")

# アカウント用エンジンとセッション
account_engine = create_engine(
    ACCOUNT_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
AccountSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=account_engine)

# アカウント用Baseクラス
AccountBase = declarative_base()

def get_account_db() -> Generator:
    """アカウント用データベースセッションを取得"""
    db = AccountSessionLocal()
    try:
        yield db
    finally:
        db.close()
