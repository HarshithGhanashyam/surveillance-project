from ultralytics import YOLO

print("[INFO] Loading YOLO model...")
model = YOLO("yolov8n.pt")

def detect_and_track(frame):
    """
    Detect and track only persons.
    Returns YOLO result object.
    """
    results = model.track(
        frame,
        persist=True,
        classes=[0],   # person only
        conf=0.5,
        verbose=False
    )

    if len(results) > 0:
        return results[0]
    return None