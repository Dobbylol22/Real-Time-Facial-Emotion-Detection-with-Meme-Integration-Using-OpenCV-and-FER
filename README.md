Real- Time Facial Emotiton Detection with Meme Overlays

Project Review:
  This project is a fun, interactive application that uses real-time facial emotion detection to display memes reflecting the user''s current emotion. It leverages AI for facial expression recognition and overlays a corresponding meme on the live video feed, making online interactions more engaging and entertaining. 

Features:
1. Real-time Emotion Detection: Detects emotions such as happy, sad, angry, and neutral using a live webcam feed.
2. Meme Overlays: Displays meme images (including animated GIFs, if supported) corresponding to the detection emotion.
3. Web Interface: Streams the live video and meme overlay on a web interface for easy accessibility.
4. dynamic Updates: Detects changes in emotion and updates the meme overlay in real-time.

Technologies Used:
1. Python: The primary programming language for backend.
2. OpenCV: For real-time video capture and image processing.
3. FER (Facial Emotion Recognition): A Python library used for detecting emotions based on facial expressions.
4. Flask: To build and serve the web application.
5. HTML & CSS: For front-end desing/
6. Github Codespaces/Visual Studio: For development and code management.

Project Setup:
Prerequisites:
1. Python 3.x
2. pip (python package installer)
3. A webcam for capturing video feed (optional if you have built in camera).

Installation:
1. Clone the repository:
      git clone https://github.com/yourusername/real-time-emotion-detection-memes.git
      cd real-time-emotion-detection-memes
2. Create a virtual environment:
      python -m venv meme_env
      source meme_env/bin/activate  # On Windows: meme_env\Scripts\activate
3. Install the required packages:
      pip install -r requirements.txt
4. Download meme Images:
   Place your meme images in the static/memes directory and ensure they match the emotion keys (e.g happy-cat.jpg/gif)

Running the Application:
1. Run the Flask App:
   python app.py
2. Access the Web Interface:
   Open your web browser and go to http://127.0.0.1:50000 to view the video live feed with meme overlays.

Usage:
 Once the app is running, the live video feed will display your face with meme overlays that change based on detected emotions. 
 The application detects various emotions, including:
  1. Happy: Displays a happy meme.
  2. Sad: Displays a sad meme.
  3. Angry: Displays a angry meme.
  4. Neutral: Displays a neutral meme.
  5. Surprise: Displays a surprise meme.
  6. Disgust: Displays a disgust meme.
  7. Fear: Displays a fear meme. 

Know Issues and Limitations:
1. Gif support: Currently, OpenCV does not support animated GIFs natively. The application may default to the first frame of the GIF or display a static image.
2. Emotion Detection Accuracy: The FER library's emotion recognition might not always be accurate in low-light conditions or for subtle ecxpressions.

Future Enhancements:
1. Add full support for GIF animations.
2. Improve emotion detection accuracy with additional training data.
3. Enhance the user interface with more responsive and interactive features.

Contributing:
  Contributions are welcome! Please open an issue or submit a pull request if you have any ideas for improvements or encounter any bugs. 

Acknowldgements:
1. FER Library: for facial expression recognition
2. OpenCV: for video and image processing capabilities
3. Special thanks to meme creators everywhere for the endless entertainment. 







