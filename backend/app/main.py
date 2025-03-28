from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from datetime import datetime

from app.database import engine, Base, get_db_engine
from app.routers import detection, history
from app.config import settings
from app.logging_config import setup_logging, logger, log_to_elasticsearch, cleanup

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        engine = get_db_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
    yield
    # Shutdown
    cleanup()

app = FastAPI(
    title="Person Detection API", 
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Setup logging
setup_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=settings.RESULTS_DIR), name="results")

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )

@app.get("/")
def read_root():
    return {
        "message": "Person Detection API is running", 
        "environment": settings.ENV
    }

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        log_data = {
            "level": "info",
            "message": f"{request.method} {request.url.path}",
            "service": "api",
            "status_code": response.status_code,
            "processing_time": process_time,
            "client_host": request.client.host,
            "@timestamp": datetime.now().isoformat()
        }
        
        log_to_elasticsearch(log_data)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        log_data = {
            "level": "error",
            "message": f"Error processing request: {str(e)}",
            "service": "api",
            "status_code": 500,
            "processing_time": process_time,
            "client_host": request.client.host,
            "@timestamp": datetime.now().isoformat()
        }
        log_to_elasticsearch(log_data)
        raise

app.include_router(detection.router)
app.include_router(history.router)