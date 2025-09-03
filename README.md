<p align="center">
  <h1 align="center" style="color:#4B8BBE;">computer-vision</h1>
  <p align="center"><em>Touchless Control with Hand Tracking — Turn Your Camera into a Virtual Mouse & Keyboard</em></p>

  <p align="center">
    <img src="https://img.shields.io/github/last-commit/gilangrizkyr/computer-vision?style=flat-square" alt="Last Commit">
    <img src="https://img.shields.io/github/languages/top/gilangrizkyr/computer-vision?style=flat-square" alt="Top Language">
    <img src="https://img.shields.io/github/languages/count/gilangrizkyr/computer-vision?style=flat-square" alt="Language Count">
    <img src="https://img.shields.io/badge/built%20with-python-blue?style=flat-square&logo=python" alt="Built with Python">
  </p>
</p>

---

## 🧭 Overview

**`computer-vision`** is a pure Python project that transforms your webcam into a **touchless input controller**.  
Using real-time hand tracking and gesture recognition, this system allows you to move the mouse cursor and simulate keyboard input **using only your hands in front of a camera** — no physical mouse or keyboard needed.

Powered by:
- 🎥 **OpenCV** – for real-time video capture and frame processing  
- 🧠 **MediaPipe** – for accurate hand landmark detection  
- 🖱️ **PyAutoGUI** – to simulate mouse and keyboard input  
- ⏱️ **time** – for timing and gesture control  

---

## ✨ Features

- 👋 **Hand Tracking** — Detects hand landmarks in real-time using MediaPipe.
- 🖱️ **Virtual Mouse** — Move your hand to control the system cursor.
- ⌨️ **Keyboard Simulation** — Use gestures to trigger keyboard events.
- 🧠 **Gesture Mapping** — Customize actions based on hand gestures.
- 🐍 **100% Python** — No external binaries or native code.

---

## 🛠 Built With

- Python 3.7+
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://google.github.io/mediapipe/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have:
- Python 3.7 or higher installed
- A webcam connected and working

### 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gilangrizkyr/computer-vision.git
   ```

2. Navigate into the project folder:
   ```bash
   cd computer-vision
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

If `requirements.txt` doesn't exist yet, create one with the following content:

```
opencv-python
mediapipe
pyautogui
```

Or install manually:

```bash
pip install opencv-python mediapipe pyautogui
```

---

## ▶️ Usage

Run the program with:

```bash
python main.py
```

> Once launched, your webcam will activate. Place your hand in front of the camera and use gestures to control your mouse or keyboard.

---

## 🧪 Testing

This project does not include automated tests yet.  
Testing is done manually by running the application and performing gestures in front of the webcam.

---


## 👤 Author

**Gilang Rizky R**  
🔗 [GitHub Profile](https://github.com/gilangrizkyr)

---

> “No keyboard. No mouse. Just hand gestures.” 👋💻
