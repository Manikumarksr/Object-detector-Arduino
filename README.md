# Object Detection with OpenCV and Ultrasound Sensor
This repository contains Python code that performs object detection using OpenCV, processes input from an ultrasound distance sensor, and provides voice output using the `pyttsx3` library. The detection model utilizes pretrained weights and class files for accurate object identification.

## Features

- **Object Detection:** Detect objects within an image using OpenCV.
- **Ultrasound Sensor Integration:** Incorporates distance measurements from an ultrasound sensor.
- **Voice Output:** Announces detected objects and distances using `pyttsx3`.


## Dependencies
- kivy
- OpenCV
- NumPy
- Matplotlib

## Usage

**Clone the Repository:**
```
git clone https://github.com/Manikumarksr/Object-detector-Arduino.git
cd Object-detector-Arduino
```

**Run the Script:**
Execute the following command to start object detection with voice feedback:
`python main.py`

## How It Works
The working sample video of this project can be found [here](https://www.youtube.com/watch?v=Yn279qkG89Ek)
**Image Capture:** The ESP-32 camera captures an image and streams it using Arduino wifi module.
**Object Detection:** The script detects objects within the image using `OpenCV`.
**Distance Measurement:** The ultrasound sensor measures the distance to the detected objects and streams it through Arduino wifi module.
**Voice Output:** The detected objects and their distances are announced via voice using `pyttsx3`.
