import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean
)

from app.db.base import Base


class TestDrive(Base):
    __tablename__ = "test_drives"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100))
    car = Column(String(100))
    drive_datetime = Column(DateTime)
    name = Column(String(100))
    phone = Column(String(20))
    has_dl = Column(Boolean, default=False)
    location = Column(String(100))

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
