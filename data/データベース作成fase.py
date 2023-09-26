import sqlite3
import config
import os
def main():
    if os.path.isfile(config.EMOTIONDATABASE):
        os.remove(config.EMOTIONDATABASE)
    # データベースに接続
    conn = sqlite3.connect(config.EMOTIONDATABASE)

    # カーソルを取得
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY,
            angry REAL,
            disgust REAL,
            fear REAL,
            happy REAL,
            sad REAL,
            surprise REAL,
            neutral REAL,
            user_name TEXT
        )
    ''')

    # 変更をコミット
    conn.commit()

    # 接続を閉じる
    conn.close()
