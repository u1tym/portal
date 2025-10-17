import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://puser:ppassword@localhost:5432/portal?client_encoding=utf8")

# 文字エンコーディングの問題を解決するため、接続パラメータを追加
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "client_encoding": "utf8"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
