import cv2

index = 0
while True:
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera {index} is available.")
    else:
        print(f"Camera {index} is not available.")
    index += 1
