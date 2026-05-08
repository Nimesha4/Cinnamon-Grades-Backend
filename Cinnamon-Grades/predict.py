from ultralytics import YOLO
import sys
from collections import Counter
import json
import cv2
import logging

# suppress YOLO logs
logging.getLogger("ultralytics").setLevel(logging.ERROR)

image_path = sys.argv[1]

# check image validity
img = cv2.imread(image_path)
if img is None:
    print(json.dumps({
        "status": "Invalid Image",
        "final_grade": None,
        "details": {}
    }))
    exit()

model = YOLO("weights/yolov11-best.pt")

results = model(image_path, conf=0.3, verbose=False)

det_list = []

for box in results[0].boxes:
    cls = int(box.cls[0])
    name = model.names[cls]
    det_list.append(name)

# no detections case
if len(det_list) == 0:
    print(json.dumps({
        "status": "No Cinnamon Detected",
        "final_grade": None,
        "details": {}
    }))
    exit()

# count grades
count = Counter(det_list)

# logic
if len(count) == 1:
    final_grade = list(count.keys())[0]
    status = "Single Grade"
else:
    final_grade = count.most_common(1)[0][0]
    status = "Mixed Grades Detected"

# final output
output = {
    "status": status,
    "final_grade": final_grade,
    "details": dict(count)
}

print(json.dumps(output))