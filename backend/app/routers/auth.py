from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.session import Session
from ..models.content import Content
from ..utils import generate_random_key, generate_session_string, generate_hash

router = APIRouter()

class GetKeyRequest(BaseModel):
    username: str

class GetKeyResponse(BaseModel):
    key: str

class LoginRequest(BaseModel):
    username: str
    key: str
    hash: str

class LoginResponse(BaseModel):
    session_string: str
    redirect_url: str

@router.post("/get-key", response_model=GetKeyResponse)
async def get_key(request: GetKeyRequest, db: Session = Depends(get_db)):
    """キー値取得API"""
    # ユーザー検索
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="アカウント不正")

    # ランダムキー値生成
    key_value = generate_random_key()

    # セッション管理テーブルにレコード追加（セッション文字列はNULL）
    session = Session(
        user_id=user.user_id,
        key_value=key_value,
        session_string=None,
        last_access_time=datetime.now()
    )
    db.add(session)
    db.commit()

    return GetKeyResponse(key=key_value)

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """ログイン認証API"""
    # ユーザー検索
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="アカウント不正")

    # セッション検索
    session = db.query(Session).filter(
        Session.user_id == user.user_id,
        Session.key_value == request.key
    ).first()
    if not session:
        raise HTTPException(status_code=401, detail="アカウント不正")

    # ハッシュ値比較
    expected_hash = generate_hash(user.password, request.key)
    if request.hash != expected_hash:
        raise HTTPException(status_code=401, detail="アカウント不正")

    # 表示順0のコンテンツ取得
    content = db.query(Content).filter(
        Content.user_id == user.user_id,
        Content.display_order == 0
    ).first()
    if not content:
        raise HTTPException(status_code=500, detail="内部処理異常")

    # セッション文字列生成・更新
    session_string = generate_session_string()
    session.session_string = session_string
    session.last_access_time = datetime.now()
    db.commit()

    return LoginResponse(
        session_string=session_string,
        redirect_url=content.redirect_url
    )
