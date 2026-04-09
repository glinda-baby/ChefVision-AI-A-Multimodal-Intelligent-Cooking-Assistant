from ultralytics import YOLO

# load YOLO model
model = YOLO("yolov8n.pt")

def detect_dish(image_path):

    results = model(image_path)

    for r in results:
        names = r.names
        cls = r.boxes.cls.tolist()

        if len(cls) > 0:
            dish = names[int(cls[0])]
            return dish

    return None