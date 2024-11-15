import cv2
import os
from flask import Flask, render_template, Response, redirect, url_for

app = Flask(__name__)

# Open the USB cameras
camera1 = cv2.VideoCapture(1)
camera2 = cv2.VideoCapture(2)

# Directory to store captured images
IMAGE_DIR = 'static/captured_images'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def gen_frames(camera):
    """Capture frames from a given camera and encode them as JPEG."""
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed1')
def video_feed1():
    """Video streaming route for Camera 1."""
    return Response(gen_frames(camera1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    """Video streaming route for Camera 2."""
    return Response(gen_frames(camera2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    """Capture images from both cameras."""
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    if ret1:
        image1_path = os.path.join(IMAGE_DIR, 'image1.jpg')
        cv2.imwrite(image1_path, frame1)

    if ret2:
        image2_path = os.path.join(IMAGE_DIR, 'image2.jpg')
        cv2.imwrite(image2_path, frame2)

    return redirect(url_for('index'))

@app.route('/')
def index():
    """Render the webpage with video feeds and capture functionality."""
    image1_path = os.path.join(IMAGE_DIR, 'image1.jpg')
    image2_path = os.path.join(IMAGE_DIR, 'image2.jpg')
    
    image1_exists = os.path.exists(image1_path)
    image2_exists = os.path.exists(image2_path)
    
    return render_template('index.html', image1_exists=image1_exists, image2_exists=image2_exists)

if __name__ == "__main__":
    app.run(debug=True)
