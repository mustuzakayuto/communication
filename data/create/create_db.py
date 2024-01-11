import sqlite3
import config
import os
def main():
    if os.path.isfile(config.DATABASE):
        os.remove(config.DATABASE)
    con = sqlite3.connect(config.DATABASE)
    cursor = con.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS  USERS (\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        nickname TEXT,\
        USERNAME TEXT  UNIQUE NOT NULL, \
        PASSWORD TEXT NOT NULL, \
        USEREMAIL TEXT NOT NULL)"  # USEREMAIL カラムを追加
    )
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
    con.commit()

    # データベース接続を閉じる
    con.close()
    print('データベースを初期化しました')



if __name__ == '__main__':
    main()
