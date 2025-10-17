import hashlib
import secrets
import string

def generate_random_key(length: int = 32) -> str:
    """ランダムなキー値を生成"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_session_string(length: int = 64) -> str:
    """ランダムなセッション文字列を生成"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hash(password: str, key: str) -> str:
    """パスワードとキー値からハッシュ値を生成"""
    combined = password + key
    return hashlib.sha256(combined.encode()).hexdigest()
