import os
import cv2
import numpy as np

REGISTERED_FACES_DIR = "data/registered_faces"


def load_face_database(face_app):
    """
    Loads all registered faces from:
    data/registered_faces/Name_RollNumber/*.jpg

    Returns:
    [
        {
            "name": "Harshith",
            "roll_no": "237Z1A0581",
            "embedding": np.array(...)
        }
    ]
    """
    face_database = []

    print(f"[INFO] Loading registered faces from: {REGISTERED_FACES_DIR}")

    if not os.path.exists(REGISTERED_FACES_DIR):
        print("[WARNING] registered_faces folder not found.")
        return face_database

    for person_folder in os.listdir(REGISTERED_FACES_DIR):
        person_path = os.path.join(REGISTERED_FACES_DIR, person_folder)

        if not os.path.isdir(person_path):
            continue

        # Expected folder name format: Name_RollNumber
        try:
            name, roll_no = person_folder.rsplit("_", 1)
        except ValueError:
            print(f"[WARNING] Skipping invalid folder name: {person_folder}")
            continue

        embeddings = []

        for image_name in os.listdir(person_path):
            if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            image_path = os.path.join(person_path, image_name)
            print(f"[INFO] Processing image: {image_path}")

            img = cv2.imread(image_path)

            if img is None:
                print(f"[WARNING] Could not read image: {image_path}")
                continue

            faces = face_app.get(img)

            if len(faces) == 0:
                print(f"[WARNING] No face found in {image_path}")
                continue

            embedding = faces[0].embedding
            embeddings.append(embedding)

        if len(embeddings) == 0:
            print(f"[WARNING] No valid face embeddings for {person_folder}")
            continue

        avg_embedding = np.mean(embeddings, axis=0)

        face_database.append({
            "name": name,
            "roll_no": roll_no,   # ✅ FIXED
            "embedding": avg_embedding
        })

        print(f"[INFO] Registered: {name} ({roll_no}) with {len(embeddings)} valid images")

    print(f"[INFO] Total registered persons: {len(face_database)}")
    return face_database