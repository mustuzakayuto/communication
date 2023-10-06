import sqlite3
import config

def rm(data_base, table, user_name,column):
    
    # SQLite3データベースに接続
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    # ユーザー名が一致する行を削除するSQLクエリを実行
    cursor.execute(f"DELETE FROM {table} WHERE {column}=?", (user_name,))

    # 変更をコミット
    conn.commit()

    # データベース接続を閉じる
    conn.close()
