from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

class Session(Base):
    __tablename__ = "sessions"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    key_value = Column(String(255), primary_key=True)
    session_string = Column(String(255), nullable=True)
    last_access_time = Column(DateTime, nullable=False)

class Content(Base):
    __tablename__ = "contents"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    display_order = Column(Integer, primary_key=True)
    content_title = Column(String(255), nullable=True)
    redirect_url = Column(String(255), nullable=False)
