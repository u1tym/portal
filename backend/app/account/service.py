from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .models import User, Session, Content
from ..core.utils import generate_random_key, generate_session_string, generate_hash


class Account:
    def __init__(self, username: str, db: Session):
        self.username = username
        self.db = db
        self.user_id: Optional[int] = None
        self.password: Optional[str] = None
        self.redirect_url: Optional[str] = None
        self.session_string: Optional[str] = None

        # ユーザー情報を取得
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            self.user_id = user.user_id
            self.password = user.password

            # 遷移先URLを取得（表示順0のコンテンツ）
            content = self.db.query(Content).filter(
                Content.user_id == user.user_id,
                Content.display_order == 0
            ).first()
            if content:
                self.redirect_url = content.redirect_url

    @staticmethod
    def check_user_exists(username: str, db: Session) -> bool:
        """ユーザ存在チェック"""
        user = db.query(User).filter(User.username == username).first()
        return user is not None

    def generate_key(self) -> Optional[str]:
        """キー値生成"""
        if not self.user_id:
            return None

        try:
            # キー値を生成
            key_value = generate_random_key()

            # セッション管理テーブルにレコードを追加
            session = Session(
                user_id=self.user_id,
                key_value=key_value,
                session_string=None,
                last_access_time=datetime.now()
            )
            self.db.add(session)
            self.db.commit()

            return key_value
        except Exception:
            self.db.rollback()
            return None

    def authenticate(self, key: str, hash_value: str) -> bool:
        """認証"""
        if not self.user_id or not self.password:
            return False

        try:
            # セッション管理情報に該当レコードがあるかチェック
            session = self.db.query(Session).filter(
                Session.user_id == self.user_id,
                Session.key_value == key
            ).first()

            if not session:
                return False

            # ハッシュ値の比較
            expected_hash = generate_hash(self.password, key)
            if hash_value != expected_hash:
                return False

            # セッション文字列を生成・更新
            self.session_string = generate_session_string()
            session.session_string = self.session_string
            session.last_access_time = datetime.now()
            self.db.commit()

            return True

        except Exception:
            self.db.rollback()
            return False

    def get_session_string(self) -> Optional[str]:
        """セッション文字列取得"""
        return self.session_string

    def get_redirect_url(self) -> Optional[str]:
        """遷移先URL取得"""
        return self.redirect_url

    def verify_session(self, session_string: str) -> bool:
        """セッション確認"""
        if not self.user_id:
            return False

        try:
            # セッション管理テーブルから該当セッション文字列を検索
            session = self.db.query(Session).filter(
                Session.user_id == self.user_id,
                Session.session_string == session_string
            ).first()

            if not session:
                return False

            # セッション文字列を再作成してDBを更新
            new_session_string = generate_session_string()
            session.session_string = new_session_string
            session.last_access_time = datetime.now()
            self.db.commit()

            # 新しいセッション文字列を保持
            self.session_string = new_session_string

            return True

        except Exception:
            self.db.rollback()
            return False
