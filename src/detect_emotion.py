import cv2
import numpy as np
from tensorflow.keras.models import load_model
import csv
from datetime import datetime
import os

# Load model and labels
model = load_model('models/emotion_model.h5', compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# CSV Logging Setup
log_path = 'emotion_log.csv'
if not os.path.exists(log_path):
    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Emotion'])

def log_emotion(emotion):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, emotion])

def detect_and_display():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (64, 64))  # updated for correct input shape
            roi = roi.astype('float32') / 255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)
            preds = model.predict(roi, verbose=0)
            emotion = emotion_labels[np.argmax(preds)]

            # Log the detected emotion
            log_emotion(emotion)

            # Draw on frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Emotion Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_display()
