import sqlite3
import os
import config
def main():
    if os.path.isfile(config.EMOTIONAVERAGEDATABASE):
        os.remove(config.EMOTIONAVERAGEDATABASE)
    # データベースに接続
    conn = sqlite3.connect(config.EMOTIONAVERAGEDATABASE)

    # カーソルを取得
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS average (
            id INTEGER PRIMARY KEY,
            angry REAL,
            disgust REAL,
            fear REAL,
            happy REAL,
            sad REAL,
            surprise REAL,
            neutral REAL
            
        )
    ''')

    # 変更をコミット
    conn.commit()

    # 接続を閉じる
    conn.close()
main()