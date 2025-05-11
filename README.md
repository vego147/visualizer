# Hand-Controlled 3D Particle Sphere

This project uses **OpenCV** and **MediaPipe** for real-time hand gesture recognition to control a dynamic 3D particle sphere built with the **Ursina Engine**.

>**Note**: A webcam is required for hand tracking to function properly.

---

## Project Structure

```
Hand-Controlled-3D-Particle-Sphere/
├── main.py                # Main application file
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Features

- Real-time hand tracking using MediaPipe
- Touch gesture detection (thumb–index pinch)
- Dynamic scaling of a 3D particle sphere
- Smooth visuals using Ursina Game Engine

---

## Requirements

> **Recommended Python Version**: 3.8 (Some versions have compatibility issues with MediaPipe)

Install dependencies with:

```bash
pip install -r requirements.txt
```

### Key Dependencies

- `opencv-python`
- `mediapipe`
- `ursina`

---

## How to Run

After installing the dependencies, run:

```bash
python main.py
```

---

## Gesture Control

- **Pinch to Toggle Scaling**: Tap your **thumb and index finger tips** to toggle the scaling mode on or off.
- When scaling is active, the **distance between the fingertips** controls the **scale** of the particle sphere in real time.

---

## Notes

- Ensure your webcam is connected and accessible.
- Run in a well-lit environment for best hand-tracking accuracy.
- Use `Ctrl+C` or press `Q` in the OpenCV window to exit.

---
