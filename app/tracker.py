def get_tracked_persons(results):
    """
    Extract tracked person detections from YOLO tracking results.
    Returns list like:
    [
        {
            "track_id": int,
            "bbox": [x1, y1, x2, y2],
            "confidence": float
        }
    ]
    """
    tracked_persons = []

    if results is None or results.boxes is None:
        return tracked_persons

    boxes = results.boxes

    for box in boxes:
        if box.id is None:
            continue

        track_id = int(box.id.item())
        conf = float(box.conf.item())
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

        tracked_persons.append({
            "track_id": track_id,
            "bbox": [x1, y1, x2, y2],
            "confidence": conf
        })

    return tracked_persons