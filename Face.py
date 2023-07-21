from flask import Flask, render_template, request, jsonify,Blueprint
from fer import FER


# インスタンス化
face = Blueprint("face",__name__)

# モデル設定
emotion_detector = FER(mtcnn=True)

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
    
    
    # 顔1つずつ入れる
    for i, face in enumerate(detected_faces):
        
        print(face)
        
        # 一番最大の感情を取得とそのスコアを取得
        emotion = max(face['emotions'], key=face['emotions'].get)
        score = face['emotions'][emotion]


    # 何か入っていれば
    if detected_faces !=[]:
        # 1つめのfaceを取得(辞書型)
        detected_faces = detected_faces[0]["emotions"]
    # 変数が入っている個数とデータ
    result = {"len":len(detected_faces),"arr":detected_faces}
    
    return jsonify(result)

