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
        "details": {},
        "message": "Invalid image file."
    }))
    exit()

model = YOLO("weights/yolov8-best.pt")

# prediction
results = model(image_path, conf=0.35, verbose=False)

# trained grades
allowed_grades = ["Alba", "C4", "C5", "H2"]

det_list = []

# no detections
if len(results[0].boxes) == 0:

    print(json.dumps({
        "status": "No Cinnamon Detected",
        "final_grade": None,
        "details": {},
        "message": "Uploaded image is not related to cinnamon."
    }))
    exit()

# process detections
for box in results[0].boxes:

    conf = float(box.conf[0])

    # ignore weak detections
    if conf < 0.45:
        continue

    cls = int(box.cls[0])
    name = model.names[cls]

    # accept only trained grades
    if name in allowed_grades:
        det_list.append(name)

# unsupported / unclear grade
if len(det_list) == 0:

    print(json.dumps({
        "status": "Unknown Grade",
        "final_grade": None,
        "details": {},
        "message": "Unable to identify this cinnamon grade accurately."
    }))
    exit()

# confidence validation
avg_conf = sum([
    float(box.conf[0])
    for box in results[0].boxes
    if float(box.conf[0]) >= 0.45
]) / len(det_list)

# unsupported / uncertain prediction
if avg_conf < 0.65:

    print(json.dumps({
        "status": "Unknown Grade",
        "final_grade": None,
        "details": {},
        "message": "This cinnamon grade is not supported or image quality is unclear."
    }))
    exit()

# count grades
count = Counter(det_list)

# determine result
if len(count) == 1:

    final_grade = list(count.keys())[0]

    output = {
        "status": "Single Grade",
        "final_grade": final_grade,
        "details": dict(count)
    }

else:

    final_grade = count.most_common(1)[0][0]

    output = {
        "status": "Mixed Grades Detected",
        "final_grade": final_grade,
        "details": dict(count),
        "message": "This bundle contains mixed cinnamon grades."
    }

# final output
print(json.dumps(output))