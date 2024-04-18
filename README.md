
# TechBoard Online

## The Problem TechBoard Online Solves
In the context of online learning environments, there is a significant challenge arising from the unavailability of digital boards during class sessions. This impediment hampers the effectiveness of teaching as educators struggle to adequately convey concepts and engage students in the absence of a suitable digital platform. Consequently, this issue hinders the seamless delivery of educational content, leading to suboptimal learning outcomes and a diminished educational experience for both teachers and students.

## Challenges We Ran Into
A major obstacle we're facing is the accurate tracking of hand gestures, exacerbated by the varied camera quality found across different devices. This challenge is particularly noticeable when striving for seamless connectivity, often resulting in lag attributable to the specifications of individual devices.

## Technologies Used
- **OpenCV**: For computer vision tasks, including hand gesture tracking.
-  **Python**: The primary programming language used for development.
- **Pickle**: For serializing and deserializing Python objects.
- **Socket**: For enabling communication between devices.

## Installation
To use TechBoard Online, follow these steps:

1. Install Python from the [official website](https://www.python.org/downloads/).
2. Install required dependencies using pip:

```bash
pip install opencv

pip install mediapipe 
##( if the module issue isn't resolved then use)
python -m pip install mediapipe --user

```

## Known Issues

1. We have to connect with the same network.
2. We have to connect through IP address.
3. Currently, the audio and video streams are running separately (but it works).
4. There is no proper UI; we are working on the UI.


