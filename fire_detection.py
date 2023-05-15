import cv2
import torch
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import numpy as np

# Email fonksiyonu
def send_email():
    email_address = "your_email@hotmail.com"  # Replace with your email
    password = "your_password"  # Replace with your email password
    to_email_address = "recipient_email@gmail.com"  # Replace with recipient's email

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email_address
    msg['Subject'] = "Fire Detected - Urgent"

    body = f"Fire detected! Location: {get_location()}"
    msg.attach(MIMEText(body, 'plain'))

    # Attach image
    attachment = open('fire_detected_image.jpg', 'rb')
    image = MIMEImage(attachment.read())
    attachment.close()
    msg.attach(image)

    try:
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(email_address, password)
        server.sendmail(email_address, to_email_address, msg.as_string())
        print("Email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to get device location (IP address based)
def get_location():
    try:
        res = requests.get('https://ipinfo.io/')
        data = res.json()
        return data
    except Exception as e:
        print(f"Error fetching location: {e}")
        return "Unknown"

# Initialize YOLO model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_best.pt')  # Replace 'yolov5s_best.pt' with the actual path to your YOLO model
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='small_fire_model.pt')
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_best.pt')

# GStreamer pipeline for Raspberry Pi camera
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# Start video capture
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
#cap = cv2.VideoCapture("ATES.MP4")
#cap = cv2.VideoCapture(0)
# Parameters
frame_width = 1280
frame_height = 720
fire_detect_count = 0

# Process frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame for processing
    frame_resized = cv2.resize(frame, (frame_width, frame_height))

    # Perform fire detection using YOLO
    results = model(frame_resized)
    detections = results.xyxy[0]  # Get the bounding boxes (x1, y1, x2, y2, confidence, class)

    fire_detected = False
    for det in detections:
        if det[5] == 0 and det[4] > 0.5:  # Class 0 is 'fire' in YOLO, confidence > 50%
            fire_detected = True
            x1, y1, x2, y2 = map(int, det[:4])  # Get the bounding box coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "Fire Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show live feed
    cv2.imshow('Fire Detection', frame)

    if fire_detected:
        fire_detect_count += 1
        print(f"Fire Detected {fire_detect_count} times")

        # Save image and send email after 50 detections
        if fire_detect_count >= 5000:
            cv2.imwrite('fire_detected_image.jpg', frame)
            send_email()  # Send email notification
            fire_detect_count = 0  # Reset counter after email sent

    # Stop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()