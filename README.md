# Portal Web Application

## 概要
ユーザー認証機能を持つWebアプリケーション

## 技術スタック
- バックエンド: Python + FastAPI
- フロントエンド: Vue3 + TypeScript
- データベース: PostgreSQL

## セットアップ

### 1. PostgreSQL起動
```bash
# ローカルでPostgreSQLを起動
net start postgresql-x64-15

# またはDockerで起動
docker run -d --name postgres -e POSTGRES_DB=portal -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
```

### 2. データベース初期化
```bash
# PostgreSQLに接続してinit.sqlを実行
psql -U user -d portal -f database/init.sql
```

### 3. バックエンド起動
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. フロントエンド起動
```bash
cd frontend
npm install
npm run dev
```

## アクセス
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API仕様書: http://localhost:8000/docs
