from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DetectionBase(BaseModel):
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0)

class DetectionCreate(DetectionBase):
    pass

class DetectionResponse(DetectionBase):
    id: int
    timestamp: datetime
    num_people: int
    original_image_path: str
    result_image_path: str

    class Config:
        from_attributes = True

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

class HistorySearchParams(PaginationParams):
    min_people: Optional[int] = Field(default=None, ge=0)
    max_people: Optional[int] = Field(default=None, ge=0)
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[DetectionResponse]

    class Config:
        from_attributes = True