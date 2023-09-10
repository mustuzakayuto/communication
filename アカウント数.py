import sqlite3

def get_db():
    print("get_db")
    db = sqlite3.connect('data/users.db')
    db.row_factory = sqlite3.Row
    return db

# データベース接続を取得
db = get_db()

# ユーザー数をカウントするSQLクエリ
query = "SELECT COUNT(*) FROM USERS;"

# クエリを実行し、結果を取得
user_count = db.execute(query).fetchone()[0]

# データベース接続を閉じる
db.close()

# 結果を表示
print("ユーザー数:", user_count)
