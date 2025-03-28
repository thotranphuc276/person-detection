from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
from datetime import datetime
import time

from app.database import get_db
from app.models import Detection
from app.schemas import DetectionResponse
from app.detector import PersonDetector
from app.config import settings
from app.logging_config import logger, log_to_elasticsearch

router = APIRouter(prefix="/detection", tags=["detection"])
detector = PersonDetector()

@router.post("/", response_model=DetectionResponse)
async def create_detection(
    file: UploadFile = File(...),
    confidence_threshold: float = Form(0.5),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    if not file.content_type.startswith("image/"):
        error_msg = "File must be an image"
        log_data = {
            "level": "error",
            "message": error_msg,
            "service": "detection",
            "file_name": file.filename,
            "content_type": file.content_type
        }
        log_to_elasticsearch(log_data)
        raise HTTPException(status_code=400, detail=error_msg)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{settings.UPLOAD_DIR}/{timestamp}_{file.filename}"
    
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detection_result = detector.detect_persons(file_name, confidence_threshold)
    process_time = time.time() - start_time

    db_detection = Detection(
        num_people=detection_result["num_people"],
        original_image_path=file_name,
        result_image_path=detection_result["result_image_path"],
        confidence_threshold=confidence_threshold
    )
    
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    log_data = {
        "level": "info",
        "message": "Person detection completed successfully",
        "service": "detection",
        "detection_id": str(db_detection.id),
        "num_people": db_detection.num_people,
        "confidence_threshold": confidence_threshold,
        "processing_time": process_time,
        "file_name": file.filename
    }
    log_to_elasticsearch(log_data)
    
    return db_detection