import sqlite3

def main(angry, disgust, fear, happy, sad, surprise, neutral, user_name,file_path):
    # データベースファイル名と接続
    conn = sqlite3.connect(file_path)

    # カーソルを取得
    cursor = conn.cursor()

    # data入れる
    cursor.execute(f'''INSERT INTO emotions (angry, disgust, fear, happy, sad, surprise, neutral, user_name)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (angry, disgust, fear, happy, sad, surprise, neutral, user_name))  # プレースホルダーを使って値を挿入
    # 変更をコミット
    conn.commit()

    # 接続を閉じる
    conn.close()
if __name__ =="__main__":
    main(0.5,0.5,0.5,0.5,0.5,0.5,0.5,"yopu","./emotions.db")
    