from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth
from . import models  # モデルをインポートしてテーブルを認識させる

app = FastAPI(title="Portal API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Portal API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
