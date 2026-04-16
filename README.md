# Surveillance Face Recognition System

## Overview

This project is a real-time surveillance system that detects and recognizes faces using YOLO and InsightFace.

## Features

* Real-time face detection
* Face recognition using embeddings
* Person identification with name and roll number
* Webcam-based tracking

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m app.main
```

## Add Faces

Place images in:

```
data/registered_faces/Name_RollNumber/
    img1.jpg
    img2.jpg
```

## Notes

* Use clear, front-facing images
* Works best in good lighting conditions
* Performance may drop in low light or extreme angles
