import sqlite3
import config
import os
def main():
    if os.path.isfile(config.IMAGEDATABASE):
        os.remove(config.IMAGEDATABASE)
    # データベースに接続
    conn = sqlite3.connect(config.IMAGEDATABASE)

    # カーソルを取得
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            image_name TEXT,
            user_name TEXT,
            prompt TEXT,
            time TEXT
        )
    ''')

    # 変更をコミット
    conn.commit()


