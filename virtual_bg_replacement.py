import cv2
import numpy as np
import mediapipe as mp
import os

# --- Load all background images from the 'backgrounds' folder ---
bg_dir = 'backgrounds'
bg_files = sorted([f for f in os.listdir(bg_dir) if f.lower().endswith(('.jpg', '.png'))])
bg_images = []
for f in bg_files:
    img = cv2.imread(os.path.join(bg_dir, f))
    if img is not None:
        resized_img = cv2.resize(img, (640, 480))
        bg_images.append(resized_img)

# Check if background images were successfully loaded
if not bg_images:
    raise FileNotFoundError("❌ No background images found in 'backgrounds/'")

# Initialize background index for switching
bg_index = 0

# --- Initialize MediaPipe Selfie Segmentation ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# --- Start capturing video from webcam ---
cap = cv2.VideoCapture(0)
print("[INFO] Press 'n' to change background, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to match background size
    frame = cv2.resize(frame, (640, 480))

    # Convert BGR to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform segmentation to separate person from background
    result = segmentor.process(rgb)
    mask = result.segmentation_mask

    # Create a binary condition mask where True = person, False = background
    condition = mask > 0.5
    condition = np.stack((condition,) * 3, axis=-1)  # Make it 3-channel

    # Get the current background image
    current_bg = bg_images[bg_index]

    # Composite the output: keep person from original frame, rest from background
    output = np.where(condition, frame, current_bg)

    # Display the final output
    cv2.imshow('Virtual Background Replacement', output)

    # Listen for keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('n'):
        bg_index = (bg_index + 1) % len(bg_images)  # Switch to next background
        print(f"[INFO] Switched to background: {bg_files[bg_index]}")
    elif key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
