import cv2
from fer import FER
# インストール系統
# pip install FER
# pip install opencv-python
# pip install --upgrade opencv-python
import datetime
import os

def main():
    # 文字の色
    character_collar = (255,97,0)
    character_size = 0.5
    
    # 画像保存名
    dirs = "image"
    # カメラにアクセスするためのキャプチャーオブジェクトを作成
    video_capture = cv2.VideoCapture(0)
    # datetimeをインスタンス化
    dt_now = datetime.datetime.now()
    # ディレクトリを設定
    Date_dir=f"{dt_now.year}_{dt_now.month}_{dt_now.day}"
    # dataフォルダーが存在するか
    if not os.path.isdir("data"):
        # フォルダー作成
        os.mkdir("data")
    # 現在の日付のフォルダーが存在するか
    if not os.path.isdir("data/"+Date_dir):
        os.mkdir("data/"+Date_dir)
        os.mkdir("data/"+Date_dir+"/"+dirs)
        os.mkdir("data/"+Date_dir+"/"+dirs+"/"+"normal")
        os.mkdir("data/"+Date_dir+"/"+dirs+"/"+"editing")
    # FERモデルの初期化
    emotion_detector = FER(mtcnn=True)

    while True:
        
            
        # カメラから1フレームずつ取得
        ret, frame = video_capture.read()

        # FERモデルを使用して表情を解析
        detected_faces = emotion_detector.detect_emotions(frame)
        print(detected_faces)
        
        # 検出された顔ごとに処理
        for i, face in enumerate(detected_faces):
            cv2.imwrite(f"data/{Date_dir}/{dirs}/normal/{dt_now.hour}_{dt_now.minute}_{dt_now.second}.png",frame)
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
            # datetimeをインスタンス化
            dt_now = datetime.datetime.now()
            # 高さの初期化
            posy=0
            # すべての種類を取得
            for emotion2 in face["emotions"]:
                # 文字列設定
                text2=emotion2+":"+str(face['emotions'][emotion2])
                # 文字を入れる
                cv2.putText(frame, text2, (x-120, y+10+(20*posy)),
                        cv2.FONT_HERSHEY_SIMPLEX, character_size, character_collar, 2)
                posy+=1
            # 画像を保存
            cv2.imwrite(f"data/{Date_dir}/{dirs}/editing/{dt_now.hour}_{dt_now.minute}_{dt_now.second}_{emotion}.png",frame)
                
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