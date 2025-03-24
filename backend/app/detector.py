import cv2
import numpy as np
from datetime import datetime
from app.config import settings

class PersonDetector:
    def __init__(self):

        self.model = cv2.dnn.readNetFromDarknet(
            "app/yolo/yolov3.cfg",
            "app/yolo/yolov3.weights"
        )
        self.layer_names = self.model.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.model.getUnconnectedOutLayers()]
        

        with open("app/yolo/coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def detect_persons(self, image_path, confidence_threshold=0.5):
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        

        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.model.setInput(blob)
        outs = self.model.forward(self.output_layers)
        

        boxes = []
        confidences = []
        class_ids = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                

                if class_id == 0 and confidence > confidence_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.4)
        

        person_count = 0
        result_image = image.copy()
        
        for i in range(len(boxes)):
            if i in indexes:
                person_count += 1
                x, y, w, h = boxes[i]
                confidence = confidences[i]
                
                cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = f"Person: {confidence:.2f}"
                cv2.putText(result_image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"{settings.RESULTS_DIR}/detection_{timestamp}.jpg"
        cv2.imwrite(result_filename, result_image)
        
        return {
            "num_people": person_count,
            "result_image_path": result_filename
        }