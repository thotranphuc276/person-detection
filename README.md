# Person Detection API

A web application for detecting people in images using YOLO object detection with OpenCV.

## Features

- Upload images for person detection
- View detection results with bounding boxes
- Display count of people detected in each image
- Browse detection history

## Tech Stack

### Backend
- FastAPI (Python)
- OpenCV with YOLO for object detection
- PostgreSQL for data storage
- SQLAlchemy for ORM

### Frontend
- Next.js
- React
- Tailwind CSS

## Project Structure

```
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── routers/      # API endpoints
│   │   ├── yolo/         # YOLO model files
│   │   ├── config.py     # Configuration settings
│   │   ├── database.py   # Database connection
│   │   ├── detector.py   # Person detection logic
│   │   ├── main.py       # FastAPI application entry point
│   │   ├── models.py     # Database models
│   │   └── schemas.py    # Pydantic schemas
│   ├── uploads/          # Uploaded images storage
│   ├── results/          # Detection results storage
│   ├── Dockerfile        # Development Docker configuration
│   └── requirements.txt  # Python dependencies
│
├── frontend/             # Next.js frontend
│   ├── src/              # Source code
│   │   ├── app/          # Next.js app directory
│   │   ├── components/   # React components
│   │   └── utils/        # Utility functions
│   ├── Dockerfile        # Development Docker configuration
│
├── nginx/                # Nginx configuration for production
├── docker-compose.yml        # Development Docker Compose
└── README.md                 # This file
```

## Setup and Running

### Prerequisites

- Docker and Docker Compose
- Git

### Development Setup

1. Download YOLOv3 model files to `backend/app/yolo/`:
   ```bash
   mkdir -p backend/app/yolo
   curl -o backend/app/yolo/yolov3.cfg https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
   curl -o backend/app/yolo/coco.names https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
   curl -o backend/app/yolo/yolov3.weights https://pjreddie.com/media/files/yolov3.weights
   ```

2. Start the development environment:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Production Setup

1. Create `.env` file with production settings:
   ```
   ENV=production
   API_BASE_URL=https://api.yourdomain.com
   DB_PASSWORD=your_secure_password
   ```

2. Start the production environment:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

## Environment Variables

### Backend
- `ENV`: Environment ('development' or 'production')
- `API_BASE_URL`: Base URL for the API
- `DATABASE_URL`: PostgreSQL connection string

### Frontend
- `NEXT_PUBLIC_API_URL`: URL of the backend API
- `NEXT_PUBLIC_ENV`: Environment ('development' or 'production')

## License

MIT 