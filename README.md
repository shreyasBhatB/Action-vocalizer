
🗣️ Action Vocalizer

**Action Vocalizer** is a real-time AI web application that detects hand signs using a custom-trained YOLOv11 model and converts them into speech using an offline text-to-speech engine. Built with Python, Flask, and OpenCV, the app enables visual-to-audio communication for accessibility, education, and gesture-based interaction.

---

FEATURES

* Real-time hand sign detection via webcam
* YOLOv11 (Ultralytics) trained on a custom Roboflow dataset
* Offline Text-to-Speech using pyttsx3
* Web interface built with Flask
* Easy to expand with more signs or languages

---

TECH STACK

* Python 3.8+
* Flask (Web Framework)
* OpenCV (Webcam & image processing)
* pyttsx3 (Offline TTS)
* Ultralytics YOLOv11 (Object Detection)
* Roboflow (Dataset creation and export)

---

PROJECT STRUCTURE

Action-vocalizer/
├── app.py                 → Main Flask application
├── best.pt                → YOLOv11 trained model
├── requirements.txt       → Python dependencies
├── templates/             → HTML pages
│   ├── index.html
│   ├── detect.html
│   ├── chat.html
│   ├── chatbot.html
│   ├── learn.html
│   └── speech\_to\_text.html
├── static/                → Static assets (CSS, JS, images)
└── README.md              → Project documentation

---

INSTALLATION

1. Clone the repository:
   git clone [https://github.com/shreyasBhatB/Action-vocalizer.git](https://github.com/shreyasBhatB/Action-vocalizer.git)
   cd Action-vocalizer

2. Install dependencies:
   pip install -r requirements.txt

3. If `pyaudio` fails to install:

   * On Windows: Use a .whl from [https://www.lfd.uci.edu/\~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
   * On macOS/Linux:
     brew install portaudio && pip install pyaudio

4. Place your trained YOLOv11 model file `best.pt` in the root directory.

---

RUNNING THE APP

Start the Flask server:
python app.py

Open your browser and go to:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

WEB ROUTES

/            → Home page
/detect      → Real-time detection with speech output
/video\_feed  → Webcam video stream
/get\_text    → Latest spoken gesture (JSON format)

---

DATASET & MODEL

* **Dataset Name**: Indian Signs
* **Created Using**: Roboflow
* **URL**: [https://app.roboflow.com/action-vocalizer/indian-signs/models/indian-signs/3](https://app.roboflow.com/action-vocalizer/indian-signs/models/indian-signs/3)
* **Format**: YOLOv8 (used with Ultralytics)
* **Model File**: best.pt (downloaded after training on Roboflow)

---

GESTURE CLASSES

The model was trained on the following 20 hand signs:

* Drink
* Food
* Good
* Grattitude
* Hello
* Home
* I love you
* Morning
* Namaste
* Night
* No
* Now
* Please
* Question
* Remember
* Sorry
* Superb
* Thank You
* Victory
* Well Done
* Yes

You can expand this list by adding more labeled images on Roboflow and retraining the model.

---

TEXT-TO-SPEECH

* Uses `pyttsx3` for offline speech synthesis
* Speaks recognized hand signs automatically
* Only speaks predictions with confidence above 0.5
* Delay and number of spoken predictions are adjustable in the `SpeechHandler` class

---

LICENSE

This project is licensed under the MIT License.
You are free to use, modify, and distribute it for personal or commercial purposes.

---

CREDITS

* YOLOv11 by Ultralytics
* Roboflow for dataset management
* pyttsx3 for offline text-to-speech
* Flask for the web framework

---

AUTHOR

Developed by **Shreyas Bhat**
GitHub: [https://github.com/shreyasBhatB](https://github.com/shreyasBhatB)

---

FUTURE IMPROVEMENTS

* [ ] Overlay gesture labels on video stream
* [ ] Add feedback UI for incorrect predictions
* [ ] Train model for full Indian Sign Language sentences
* [ ] Integrate voice command responses
* [ ] Dockerize for easy deployment
* [ ] Mobile/tablet-friendly interface

---

CORE DEPENDENCIES

Flask
opencv-python
ultralytics
pyttsx3
SpeechRecognition
pyaudio (manual install may be required)

