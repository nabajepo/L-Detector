# L-Detector – Real-Time Face, Object & Micro-Expression Detection (Python)

## Overview
**L-Detector** is an AI-powered detection application built with **Python** that can detect:

- **Faces** (recognition-style search in a folder/database)
- **Objects** (object detection)
- **Micro-expressions** (facial expression detection)

It supports multiple input modes:
- **Images**
- **Videos**
- **Webcam**
- **Screen / Real-time GUI monitoring (PyQt5)**

This project demonstrates real-time computer vision pipelines using **OpenCV + TensorFlow + DeepFace**, integrated into a **PyQt5 GUI**.

---

## Features

### Face Detection / Search
- **Images:** provide a face (or faces) and search for matching faces inside an image folder (database-like behavior)
- **Videos:** detect/search faces inside a user-provided video
- **Webcam:** detect/search faces using the camera

### Object Detection
- **Images:** search for specific objects in a folder of images (the app shows the list of detectable objects)
- **Videos:** detect objects in a video (`all` option detects all objects)
- **Webcam:** detect objects using the camera

### Micro-Expression Detection
- **Images:** search for images matching a selected expression (list provided by the app)
- **Videos:** detect all expressions or a specific expression in a video
- **Webcam:** detect expressions in real time using the camera

### Screen / GUI Real-Time Detection (PyQt5)
- Real-time detection through a **PyQt5 interface**
- Continuous monitoring mode (useful for demos and live visualization)

---

## Demo
A video demonstration is available here:
- https://youtube.com/playlist?list=PL-wv9I8aC6IkTB4MaiHGUeZvYV_jSHiu0&si=eMMdp4B9cc6gJDEQ

---

## Requirements

### Python Version
- **Python 3.8 to 3.12**

### TensorFlow Version
- **TensorFlow 2.11 to 2.17**

---

## Run locally
From the repository root(L-Detector/classes/) : 
```bash
pip install -r requirements.txt
python main.py
```
