import numpy as np

RECOGNITION_THRESHOLD = 0.75  # adjust if needed


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recognize_face(face_crop, face_app, face_database):
    """
    Recognize one face crop against registered database.
    Returns:
        (name, roll_no, score)
    """
    if face_crop is None or face_crop.size == 0:
        return "Unknown", "N/A", 0.0

    # Prevent crash on very small crops
    h, w = face_crop.shape[:2]
    if h < 80 or w < 80:
        return "Unknown", "N/A", 0.0

    try:
        faces = face_app.get(face_crop)
    except Exception as e:
        print(f"[WARNING] Face recognition skipped: {e}")
        return "Unknown", "N/A", 0.0

    if len(faces) == 0:
        return "Unknown", "N/A", 0.0

    emb = faces[0].embedding

    best_score = -1
    best_person = None

    for person in face_database:
        db_emb = person["embedding"]

        name = person.get("name", "Unknown")
        roll_no = person.get("roll_no", "N/A")

        score = cosine_similarity(emb, db_emb)

        print(f"[DEBUG] Comparing with {name} ({roll_no}): {score:.4f}")

        if score > best_score:
            best_score = score
            best_person = person

    print(f"[DEBUG] Best score: {best_score:.4f}")

    if best_score >= RECOGNITION_THRESHOLD and best_person is not None:
        return (
            best_person.get("name", "Unknown"),
            best_person.get("roll_no", "N/A"),
            best_score
        )

    return "Unknown", "N/A", best_score