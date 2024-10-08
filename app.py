from flask import Flask, render_template, Response, jsonify
from collections import deque
import cv2
from fer import FER
import os
from PIL import Image, ImageSequence
import numpy as np

app = Flask(__name__)

#initialize the few face detector
face_detector = FER()

#Initialize a queue to hold the last fer predictions.
predictions = deque(maxlen=5)

meme_dict = {
    'happy': 'static/memes/happy-cat.gif',
    'angry': 'static/memes/angry.jpg',
    'sad': 'static/memes/sad-cat.gif',
    'neutral': 'static/memes/neutral.jpg',
    'fear': 'static/memes/surprise-cat.gif',
    'surprise': 'static/memes/surprise-cat.gif',
    'disgust': 'static/memes/disgust-cat.gif'
}

def detect_emotion(frame):
    result = face_detector.detect_emotions(frame)
    if result:
        emotion_data = result[0]['emotions']
        return max(emotion_data,key=emotion_data.get)
    return None

#OpenCV function to capture live video feed from the webcam.
camera = cv2.VideoCapture(0) # pylint: disable=E1101
current_emotion = 'neutral'
if not camera.isOpened():
    print("Error: Could not open camera")

def overlay_meme(frame, meme_path):
    #check if the file is a GIF:
    if meme_path.endswith('.gif'):
        #load the gif using PIL
        gif = Image.open(meme_path)
        #extract the first frame of the gif
        gif_frame = next(ImageSequence.Iterator(gif))
        #convert the gif frame to numpy array
        gif_frame_np = np.array(gif_frame.convert("RGBA"))
        #convert the gif frame to fit the desired area
        gif_frame_resized = cv2.resize(gif_frame_np, (150,150))
        #convert the resized frame back to OpenCV format
        gif_frame_resized = cv2.cvtColor(gif_frame_resized, cv2.COLOR_RGBA2BGRA)
        #get the position to overlay the gif
        x_offset, y_offset = 50,50
        for c in range(0, 3):
            frame[y_offset: y_offset + gif_frame_resized.shape[0], x_offset:x_offset + gif_frame_resized.shape[1], c] = \
            gif_frame_resized[:, :, c] * (gif_frame_resized[:, :, 3] / 255.0) + \
            frame[y_offset:y_offset + gif_frame_resized.shape[0], x_offset:x_offset + gif_frame_resized.shape[1], c] * (1.0 - gif_frame_resized[:, :, 3] / 255.0)

    else:
        #Load the meme image using OpenCV
        meme_img = cv2.imread(meme_path, cv2.IMREAD_UNCHANGED)
        if meme_img is not None:
            if meme_img.shape[2] == 4:
                #Resize meme to fit the face or specific location
                meme_img = cv2.resize(meme_img, (150,150))
                #Get the position to overlay
                x_offset, y_offset = 50,50
                for c in range(0,3):
                    frame[y_offset: y_offset + meme_img.shape[0], x_offset:x_offset + meme_img.shape[1],c] = \
                    meme_img[:, :, c] * (meme_img[:, :, 3] / 255.0) + \
                    frame[y_offset:y_offset + meme_img.shape[0], x_offset:x_offset + meme_img.shape[1], c] * (1.0 - meme_img[:, :, 3] / 255.0)
            else:
                meme_img = cv2.resize(meme_img, (150,150))
                x_offset, y_offset = 50,50
                frame[y_offset:y_offset + meme_img.shape[0], x_offset:x_offset + meme_img.shape[1]] = meme_img   
    return frame
#Capture video feed
def gen_frames():
    global current_emotion
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
                   #Get the corresponding meme path 
                    meme_path = meme_dict.get(most_common_emotion, 'static/memes/neutral.jpg')
                    frame = overlay_meme(frame, meme_path)
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

@app.route('/current_meme',methods=['GET'])
def current_meme_route():
    """Return the current meme path based on the most common emotion"""
    global current_emotion
    meme_path = meme_dict.get(current_emotion, 'static/memes/neutral.jpg')
    return jsonify({'meme_path':meme_path})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) #Bind to 0.0.0.0 and specify the port if needed. 
