import sqlite3
def get(data_base,table):
    print()
    print("_____"+data_base,table+"________")
    # データベースに接続
    conn = sqlite3.connect(data_base)

    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリを実行
    cursor.execute("SELECT * FROM "+table)

    # 結果を取得
    data = cursor.fetchall()
    # print(data)
    # データを処理
    for row in data:
        print(row)

    # データベース接続を閉じる
    conn.close()
