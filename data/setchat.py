import sqlite3
import config

def create_room_all():
    conn = sqlite3.connect(config.CHATDATABASE)
    cursor = conn.cursor()

    # チャットルームの名前（room）を指定します。ここでは "bare" としますが、任意の名前を選択できます。
    room_name = "全員参加可能"

    # チャットルームを作成
    cursor.execute("INSERT INTO chat (user_id1, user_id2, room) VALUES (?, ?, ?)", (0, 0, room_name))
    conn.commit()

    conn.close()