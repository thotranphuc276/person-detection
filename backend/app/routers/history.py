from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database import get_db
from app.models import Detection
from app.schemas import DetectionResponse, PaginatedResponse, HistorySearchParams
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=PaginatedResponse)
def get_detection_history(
    search_params: HistorySearchParams = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(Detection)
    
    filters = []
    
    if search_params.min_people is not None:
        filters.append(Detection.num_people >= search_params.min_people)
    
    if search_params.max_people is not None:
        filters.append(Detection.num_people <= search_params.max_people)
    
    if search_params.date_from is not None:
        filters.append(Detection.timestamp >= search_params.date_from)
    
    if search_params.date_to is not None:
        filters.append(Detection.timestamp <= search_params.date_to)
    
    if filters:
        query = query.filter(and_(*filters))
    
    total = query.count()
    total_pages = (total + search_params.limit - 1) // search_params.limit
    
    skip = (search_params.page - 1) * search_params.limit
    query = query.order_by(Detection.timestamp.desc()).offset(skip).limit(search_params.limit)
    
    logging.debug(f"Total detections: {total}")
    logging.debug(f"Total pages: {total_pages}")
    logging.debug(f"Current page: {search_params.page}")
    logging.debug(f"Items per page: {search_params.limit}")
    
    return {
        "total": total,
        "page": search_params.page,
        "limit": search_params.limit,
        "total_pages": total_pages,
        "items": query.all()
    }

@router.get("/{detection_id}", response_model=DetectionResponse)
def get_detection_by_id(detection_id: int, db: Session = Depends(get_db)):
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    return detection