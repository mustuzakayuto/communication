from flask import Flask, render_template, request, jsonify
import base64
import cv2
import datetime
from fer import FER
import numpy as np
import os
import json
app = Flask(__name__)
app.debug = True
app.template_folder = 'template'


emotion_detector = FER(mtcnn=True)


@app.route('/')
def index():
    return render_template('Facial_Expression_Analysis.html')
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

@app.route('/upload', methods=['POST'])
def upload():
    
    frame = request.json['frame']
    
    detected_faces = emotion_detector.detect_emotions(frame)
    
    
    
    for i, face in enumerate(detected_faces):
        
        print(face)
        
        
        emotion = max(face['emotions'], key=face['emotions'].get)
        score = face['emotions'][emotion]

        x, y, w, h = face['box']

        text = f"{emotion}: {score:.2f}"
        

        dt_now = datetime.datetime.now()
        posy = 0
        for emotion2 in face["emotions"]:
            text2 = emotion2 + ":" + str(face['emotions'][emotion2])
            
            posy += 1

        
    if detected_faces !=[]:
        detected_faces = detected_faces[0]["emotions"]
    result = {"len":len(detected_faces),"arr":detected_faces}
    
    return jsonify(result)

if __name__ == '__main__':
    app.run()
