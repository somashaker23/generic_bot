import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Text
)

from app.db.base_class import Base


class CallbackRequest(Base):
    __tablename__ = "callback_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    reason = Column(Text)
    preferred_time = Column(String(50))
    status = Column(String(20), default="pending")
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
