from flask import Flask, render_template, Response
from collections import deque
import cv2
from fer import FER

app = Flask(__name__)

#initialize the few face detector
face_detector = FER()

#Initialize a queue to hold the last fer predictions.
predictions = deque(maxlen=5)

def detect_emotion(frame):
    result = face_detector.detect_emotions(frame)
    if result:
        emotion_data = result[0]['emotions']
        return max(emotion_data,key=emotion_data.get)
    return None

#OpenCV function to capture live video feed from the webcam.
camera = cv2.VideoCapture(0) # pylint: disable=E1101

def gen_frames():
    while True:
        #Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            print("Failed to capture frame")
            break
        else:
            #Detect emotion in the current frame
            current_emotion = detect_emotion(frame)
            if current_emotion:
                #Add the current prediction to the queue
                predictions.append(current_emotion)

                if predictions:
                    #determine the most frequent emotion in the last few predictions
                    most_common_emotion = max(set(predictions), key= predictions.count)
                    #Display the emotion of the video frame
                    emotion_text = f"Emotion: {most_common_emotion}"
                else:
                    emotion_text = "Emotion: Unknown"
                
                cv2.putText(frame, emotion_text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            #Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg',frame)
            if not ret:
                print("Failed to encode frame")
            frame = buffer.tobytes()

            #yield the frame in byte format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
            
@app.route('/')
def index():
    """Render the main page with the video feed"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)