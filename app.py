from flask import Flask, Response, render_template, jsonify, request
import pyttsx3
import time
import cv2
from ultralytics import YOLO

app = Flask(__name__)
detected_text = ""  # Global variable to store detected text
player_turn = 1  # Keep track of whose turn it is (1 for Player 1, 2 for Player 2)
chat_history = []  # List to store the chat messages (hand signs or text)
hand_sign_detection_paused = False  # Flag to pause hand sign detection

class SpeechHandler:
    def __init__(self, delay=2, predictions_to_speak=3):
        self.engine = pyttsx3.init()
        self.last_time_spoken = time.time()
        self.delay = delay
        self.predictions_to_speak = predictions_to_speak

    def speak_predictions(self, predictions):
        global detected_text
        current_time = time.time()
        if current_time - self.last_time_spoken >= self.delay:
            detected_text = ", ".join(predictions)  # Update detected text
            for prediction in predictions[:self.predictions_to_speak]:
                print(f"Predicted: {prediction}")
                self.engine.say(prediction)
                self.engine.runAndWait()
            self.last_time_spoken = current_time

def generate_frames():
    global detected_text, player_turn, chat_history, hand_sign_detection_paused
    model = YOLO('best.pt')  # Replace with your model path
    speech_handler = SpeechHandler()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    frame_rate = 1
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Pause hand sign detection if flag is set
        if hand_sign_detection_paused:
            time.sleep(1)  # Sleep for a while when detection is paused
            continue

        current_time = time.time()
        if current_time - prev_time >= frame_rate:
            results = model(frame)

            predictions = []
            for box in results[0].boxes:
                label = results[0].names[int(box.cls)]
                confidence = float(box.conf)
                if confidence > 0.5:
                    predictions.append(label)

            if predictions:
                speech_handler.speak_predictions(predictions)

                # Update chat history with the player's hand sign
                if player_turn == 1:
                    chat_history.append(f"Player 1 (Hand Signs): {', '.join(predictions)}")
                    player_turn = 2  # Switch to Player 2's turn
                else:
                    chat_history.append(f"Player 2 (Typing/Speaking): {', '.join(predictions)}")
                    player_turn = 1  # Switch to Player 1's turn

            prev_time = current_time

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

@app.route('/chat')
def chat():
    """New route for the chat page."""
    return render_template('chat.html', chat_history=chat_history)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_text')
def get_text():
    """Endpoint to get the detected text."""
    return jsonify({"text": detected_text})
#
# @app.route('/get_chat_history')
# def get_chat_history():
#     """Endpoint to get the chat history."""
#     return jsonify({"chat_history": chat_history})
#
# @app.route('/player2_message', methods=['POST'])
# def player2_message():
#     """Endpoint for Player 2 to send a typed or spoken message."""
#     global player_turn, hand_sign_detection_paused
#     message = request.json.get('message')
#     if player_turn == 2:
#         chat_history.append(f"Player 2 (Typing/Speaking): {message}")
#         player_turn = 1  # Switch back to Player 1
#         hand_sign_detection_paused = False  # Resume hand sign detection
#         return jsonify({"status": "success", "message": message})
#     else:
#         hand_sign_detection_paused = True  # Pause hand sign detection
#         return jsonify({"status": "error", "message": "It's not Player 2's turn."})

@app.route('/stop_hand_sign_detection', methods=['POST'])
def stop_hand_sign_detection():
    """Stop hand sign detection temporarily."""
    global hand_sign_detection_paused
    hand_sign_detection_paused = True  # Pause detection
    return jsonify({"status": "success", "message": "Hand sign detection paused."})

@app.route('/resume_hand_sign_detection', methods=['POST'])
def resume_hand_sign_detection():
    """Resume hand sign detection."""
    global hand_sign_detection_paused
    hand_sign_detection_paused = False  # Resume detection
    return jsonify({"status": "success", "message": "Hand sign detection resumed."})

# @app.route('/speech_to_text')
# def speech_to_text():
#     """Page for real-time speech-to-text functionality."""
#     return render_template('speech_to_text.html')

####Speech


import speech_recognition as sr
import threading



speech_text = ""  # Global variable to store live speech-to-text data

def listen_to_speech():
    """Continuously listens for speech and updates the global speech_text."""
    global speech_text
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Calibrating microphone for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Listening for speech...")
            while True:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    # Recognize speech using Google's speech-to-text
                    speech_text = recognizer.recognize_google(audio)
                    print(f"Recognized Speech: {speech_text}")
                except sr.UnknownValueError:
                    speech_text = "Couldn't understand the audio."
                except sr.RequestError as e:
                    speech_text = "Speech Recognition error. Check your internet connection."
    except Exception as e:
        print(f"Error initializing microphone: {e}")
        speech_text = "Error initializing microphone."


intents = {
    "hello": "Hello! How can I help you?",
    "help": "This system converts hand signs into words. Please make a sign.",
    "thanks": "You're welcome!",
}

@app.route('/chatbot')
def chatbot():
    """Page for the chatbot with hand sign recognition integration."""
    return render_template('chatbot.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    """Endpoint for Player 2 to send messages."""
    global player_turn, hand_sign_detection_paused
    message = request.json.get('message', '').strip()
    if player_turn == 2 and message:
        chat_history.append(f"Player 2 (Typing): {message}")
        player_turn = 1  # Switch back to Player 1
        hand_sign_detection_paused = False  # Resume hand sign detection
        return jsonify({"status": "success", "message": message})
    return jsonify({"status": "error", "message": "It's not Player 2's turn or message is empty."})
@app.route('/speech_to_text_feed')
def speech_to_text_feed():
    """Endpoint to fetch live speech-to-text data."""
    global speech_text
    return jsonify({"speech_text": speech_text})

@app.route('/speech_to_text')
def speech_to_text_page():
    """Page to display real-time speech-to-text functionality."""
    return render_template('speech_to_text.html')


@app.route('/learn')
def learn():
    return render_template('learn.html')  # Template where YouTube links are listed

if __name__ == '__main__':
    # Start speech recognition in a background thread
    # speech_thread = threading.Thread(target=listen_to_speech, daemon=True)
    # speech_thread.start()

    # Run Flask application
    app.run(debug=True)