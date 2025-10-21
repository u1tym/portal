from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .config import get_account_db
from .service import Account

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
async def get_key(request: GetKeyRequest, db: Session = Depends(get_account_db)):
    """キー値取得API"""
    # ユーザー存在チェック
    if not Account.check_user_exists(request.username, db):
        raise HTTPException(status_code=401, detail="アカウント不正")

    # Accountインスタンス作成
    account = Account(request.username, db)

    # キー値生成
    key_value = account.generate_key()
    if not key_value:
        raise HTTPException(status_code=500, detail="内部処理異常")

    return GetKeyResponse(key=key_value)

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_account_db)):
    """ログイン認証API"""
    # Accountインスタンス作成
    account = Account(request.username, db)

    # 認証処理
    if not account.authenticate(request.key, request.hash):
        raise HTTPException(status_code=401, detail="アカウント不正")

    # 遷移先URL取得
    redirect_url = account.get_redirect_url()
    if not redirect_url:
        raise HTTPException(status_code=500, detail="内部処理異常")

    # セッション文字列取得
    session_string = account.get_session_string()
    if not session_string:
        raise HTTPException(status_code=500, detail="内部処理異常")

    return LoginResponse(
        session_string=session_string,
        redirect_url=redirect_url
    )
