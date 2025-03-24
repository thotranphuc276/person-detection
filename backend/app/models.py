from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    num_people = Column(Integer)
    original_image_path = Column(String)
    result_image_path = Column(String)
    confidence_threshold = Column(Float, default=0.5)
