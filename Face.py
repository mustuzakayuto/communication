# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify,Blueprint,session
from fer import FER
import pandas as pd
import sqlite3
import face_preservation
import face_average
import config
# インスタンス化
face = Blueprint("face",__name__)
emotions_data_base=config.EMOTIONDATABASE
# モデル設定
try:
    
    emotion_detector = FER(mtcnn=True)
    
    # Load the model here
except UnicodeDecodeError as e:
    print("UnicodeDecodeError:", e)

# (ipアドレス:5000)/face_emotionと入力で表示
@face.route('/face_emotion')
def face_emotion():
    
    return render_template('face.html')

# エラー対策
@face.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

@face.route('/upload', methods=['POST'])
def upload():
    # 受け取ったframeをframe変数に入れる
    frame = request.json['frame']
    
    # 画像の中の顔の検索してそれを辞書型の変数に入れる
    detected_faces = emotion_detector.detect_emotions(frame)
    
    # 何か入っていれば
    if detected_faces !=[]:
        # 1つめのfaceを取得(辞書型)
        detected_faces = detected_faces[0]["emotions"]
        
        
        face_preservation.main(detected_faces["angry"],detected_faces["disgust"],detected_faces["fear"],detected_faces["happy"],detected_faces["sad"],detected_faces["surprise"],detected_faces["neutral"],session['username'],emotions_data_base)
    
        
        
        
            
    # 変数が入っている個数とデータ
    result = {"len":len(detected_faces),"arr":detected_faces}
    
    return jsonify(result)

@face.route('/average', methods=['POST'])
def average():
    

    # nameが同じ行を取得
    name = session['username']  # ここに検索したいnameを指定
    
    
    column_means = face_average.main(emotions_data_base,name)
    maxface=0
    expression =""
    for face,averagedata in column_means.items():
        if averagedata>maxface:
            maxface=averagedata
            expression=face
    # column_means = column_means.reset_index()
    print(column_means)
    print(expression,maxface)
    decimal_point = 2
    # 結果を表示
    result = {
            
            "angry":round(column_means["angry"],decimal_point),
            "disgust":round(column_means["disgust"],decimal_point),
            "fear":round(column_means["fear"],decimal_point),
            "happy":round(column_means["happy"],decimal_point),
            "sad":round(column_means["sad"],decimal_point),
            "surprise":round(column_means["surprise"],decimal_point),
            "neutral":round(column_means["neutral"],decimal_point) ,
            "expression":expression,
            "maxface":maxface
                }  
    face_preservation.main2(result["angry"],result["disgust"],result["fear"],result["happy"],result["sad"],result["surprise"],result["neutral"],"data/emotionaverage.db")
    print(result)
    # データ削除
    # import face初期化
    # face初期化.main(csvfile)
    
    return jsonify(result)