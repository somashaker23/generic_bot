import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Text,
    DECIMAL
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(20), unique=True, nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    variant = Column(String(100))
    type = Column(String(50))
    year = Column(Integer)
    fuel_type = Column(String(20))
    transmission = Column(String(20))
    mileage = Column(Integer)
    price = Column(DECIMAL(12, 2))
    color = Column(String(30))
    engine_cc = Column(Integer)
    power_bhp = Column(Integer)
    seats = Column(Integer)
    description = Column(Text)
    status = Column(String(20), default="available")

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    images = relationship("CarImage", back_populates="car", cascade="all, delete")
