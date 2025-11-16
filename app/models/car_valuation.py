import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, DECIMAL
)

from app.db.base import Base


class CarValuation(Base):
    __tablename__ = "car_valuations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100))
    name = Column(String(100))
    phone = Column(String(20))

    brand = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    fuel_type = Column(String(20))
    owner = Column(String(20))
    condition = Column(String(20))
    location = Column(String(100))

    estimated_value = Column(DECIMAL(12, 2))

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
