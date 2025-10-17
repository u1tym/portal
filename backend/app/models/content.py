from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Content(Base):
    __tablename__ = "contents"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    display_order = Column(Integer, primary_key=True)
    content_title = Column(String(255), nullable=True)
    redirect_url = Column(String(255), nullable=False)
