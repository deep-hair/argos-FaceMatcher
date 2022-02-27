import cv2

def gen_frames():
    camera = cv2.VideoCapture('rtsp://admin:SFYZEV@78.113.98.174:554/H.264')
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')