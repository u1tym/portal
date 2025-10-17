from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..core.database import get_db

router = APIRouter()

class ScheduleRequest(BaseModel):
    username: str
    hash_value: str

class ScheduleResponse(BaseModel):
    success: bool
    hash_value: str

@router.post("/get-schedule", response_model=ScheduleResponse)
async def get_schedule(request: ScheduleRequest, db: Session = Depends(get_db)):
    """スケジュール取得API"""
    # 暫定実装：成否としてOKと、そのままのハッシュ値を返す
    return ScheduleResponse(
        success=True,
        hash_value=request.hash_value
    )
