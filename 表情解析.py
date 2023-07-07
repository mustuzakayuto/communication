import cv2
from fer import FER
# インストール系統
# pip install FER
# pip install opencv-python
# pip install --upgrade opencv-python
import datetime
import os
character_collar = (255,97,0)
def main():
    
    # フレーム数ごとに取得
    frame_rate=5
    frame_number = 0
    dirs = "image"
    # カメラにアクセスするためのキャプチャーオブジェクトを作成
    video_capture = cv2.VideoCapture(0)
    dt_now = datetime.datetime.now()
    Date_dir=f"{dt_now.year}_{dt_now.month}_{dt_now.day}"
    if not os.path.isdir("data/"+Date_dir):
        os.mkdir("data/"+Date_dir)
        os.mkdir("data/"+Date_dir+"/"+dirs)
    # FERモデルの初期化
    emotion_detector = FER(mtcnn=True)

    while True:
        if frame_number%frame_rate==0:
            
            # カメラから1フレームずつ取得
            ret, frame = video_capture.read()

            # FERモデルを使用して表情を解析
            detected_faces = emotion_detector.detect_emotions(frame)
            print(detected_faces)
            
            # 検出された顔ごとに処理
            for i, face in enumerate(detected_faces):
                print(i)
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
                dt_now = datetime.datetime.now()
                
                posy=0
                for emotion2 in face["emotions"]:
                    text2=emotion2+":"+str(face['emotions'][emotion2])
                    cv2.putText(frame, text2, (x-120, y+(20*posy)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, character_collar, 2)
                    posy+=1
                
                cv2.imwrite(f"data/{Date_dir}/{dirs}/{dt_now.hour}_{dt_now.minute}_{dt_now.second}_{emotion}.png",frame)
                
        frame_number+=1
        # フレームを表示
        cv2.imshow('Emotion Detection', frame)

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    # キャプチャーオブジェクトを解放
    video_capture.release()

    # ウィンドウを閉じる
    cv2.destroyAllWindows()

if __name__ =="__main__":
    main()