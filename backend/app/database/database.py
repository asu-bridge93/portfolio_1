"""
データベース → お弁当箱（データを入れておく場所）
engine → お弁当箱を開けるカギ
SessionLocal → お弁当を食べるときに使うお箸
get_db() → お箸を貸して、食べ終わったら片付けるルール
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベース接続URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./predictions.db"
)

# sqlalchemyエンジンの作成（データベースとつながる準備）
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# sessionファクトリー（データベースに入れる・取り出すための道具を作る）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースを使うときのルール
def get_db():
    """FastAPIのエンドポイントで使用するデータベースsession"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
