import cv2
from fer import FER

# pip install FER
# pip install opencv-python
# pip install --upgrade opencv-python
# カメラにアクセスするためのキャプチャーオブジェクトを作成
video_capture = cv2.VideoCapture(0)

# FERモデルの初期化
emotion_detector = FER(mtcnn=True)

while True:
    # カメラから1フレームずつ取得
    ret, frame = video_capture.read()

    # FERモデルを使用して表情を解析
    detected_faces = emotion_detector.detect_emotions(frame)
    print(detected_faces)
    
    # 検出された顔ごとに処理
    for face in detected_faces:
        # 表情とそのスコアを取得
        emotion = max(face['emotions'], key=face['emotions'].get)
        score = face['emotions'][emotion]

        # 顔領域に枠を描画
        x, y, w, h = face['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 解析結果を表示
        text = f"{emotion}: {score:.2f}"
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # フレームを表示
    cv2.imshow('Emotion Detection', frame)

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャーオブジェクトを解放
video_capture.release()

# ウィンドウを閉じる
cv2.destroyAllWindows()
