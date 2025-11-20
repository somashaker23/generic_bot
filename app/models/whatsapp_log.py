from sqlalchemy import Column, Integer, String, DateTime
import datetime
from app.db.base_class import Base


class WhatsAppLog(Base):
    __tablename__ = "whatsapp_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    message = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # incoming/outgoing
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
