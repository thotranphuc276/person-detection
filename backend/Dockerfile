FROM python:3.9-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir -p app/yolo


RUN mkdir -p /tmp/yolo_download && cd /tmp/yolo_download \
    && apt-get update && apt-get install -y wget \
    && wget https://pjreddie.com/media/files/yolov3.weights -O /app/app/yolo/yolov3.weights \
    && wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg -O /app/app/yolo/yolov3.cfg \
    && wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names -O /app/app/yolo/coco.names \
    && rm -rf /tmp/yolo_download


COPY . .


RUN mkdir -p uploads results


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]