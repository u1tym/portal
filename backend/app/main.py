from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .account import routers as account_routers
from .account import models  # モデルをインポートしてテーブルを認識させる
from .schedule import routers as schedule_routers
from .bank import routers as bank_routers
from .bank import models as bank_models  # 銀行管理モデルをインポート

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
app.include_router(account_routers.router, prefix="/api", tags=["account"])
app.include_router(schedule_routers.router, prefix="/api", tags=["schedule"])
app.include_router(bank_routers.router, prefix="/api", tags=["bank"])

@app.get("/")
async def root():
    return {"message": "Portal API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
