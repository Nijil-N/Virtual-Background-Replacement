# Virtual Background Replacement

This Python script uses **MediaPipe Selfie Segmentation** to replace the webcam background in real-time, similar to virtual backgrounds in video calls.

## Features

* Real-time person segmentation using MediaPipe.
* Replace the background with custom images.
* Switch between multiple background images with a key press.

## Requirements

Install the required libraries:

pip install opencv-python mediapipe numpy


## Setup

1. Create a folder named `backgrounds` in the same directory as the script.
2. Add `.jpg` or `.png` images into the `backgrounds` folder. These will be used as backgrounds.
3. Make sure your webcam is connected and working.

## Usage

Run the script:

python your_script_name.py


### Controls

* Press **`n`** to switch to the next background.
* Press **`q`** to quit the program.

## Notes

* All background images will be resized to 640x480.
* Person segmentation works best in well-lit conditions with a clear view of the subject.

