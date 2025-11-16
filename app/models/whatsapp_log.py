from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class WhatsAppLog(Base):
    __tablename__ = "whatsapp_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # incoming/outgoing
    created_at = Column(DateTime, default=datetime.utcnow)
