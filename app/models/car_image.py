import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CarImage(Base):
    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    image_path = Column(String(255), nullable=False)
    image_type = Column(String(20), nullable=False)
    image_index = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    car = relationship("Car", back_populates="images")

