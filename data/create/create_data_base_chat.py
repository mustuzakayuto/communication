import sqlite3
import config
import os
def main():
    if os.path.isfile(config.CHATDATABASE):
        os.remove(config.CHATDATABASE)
    # データベースに接続
    conn = sqlite3.connect(config.CHATDATABASE)
    cursor = conn.cursor()

    # userテーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            nickname TEXT
        )
    ''')

    # chatテーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id1 INTEGER,
            user_id2 INTEGER,
            room TEXT,
            is_group BOOLEAN
            
        )
    ''')

    # chatmessテーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatmess (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            to_user INTEGER,
            from_user INTEGER,
            message TEXT,
            time TEXT,
            type TEXT
        )
    ''')

    # データベースへの変更を保存
    conn.commit()

    # データベース接続を閉じる
    conn.close()