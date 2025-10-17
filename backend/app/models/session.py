from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Session(Base):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    key_value = Column(String(255), primary_key=True)
    session_string = Column(String(255), nullable=True)
    last_access_time = Column(DateTime, nullable=False)
