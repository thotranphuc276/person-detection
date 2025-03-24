from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
from datetime import datetime

from app.database import get_db
from app.models import Detection
from app.schemas import DetectionResponse
from app.detector import PersonDetector
from app.config import settings

router = APIRouter(prefix="/detection", tags=["detection"])
detector = PersonDetector()

@router.post("/", response_model=DetectionResponse)
async def create_detection(
    file: UploadFile = File(...),
    confidence_threshold: float = Form(0.5),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{settings.UPLOAD_DIR}/{timestamp}_{file.filename}"
    
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detection_result = detector.detect_persons(file_name, confidence_threshold)

    db_detection = Detection(
        num_people=detection_result["num_people"],
        original_image_path=file_name,
        result_image_path=detection_result["result_image_path"],
        confidence_threshold=confidence_threshold
    )
    
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    return db_detection