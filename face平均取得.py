import sqlite3
def main(file_path,name):
    # データベースファイル名と接続
    conn = sqlite3.connect(file_path)

    # カーソルを取得
    cursor = conn.cursor()

    # テーブル名と対応するカラム名を設定
    table_name = 'emotions'  # テーブル名を設定
    column_names = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral','user_name']  # カラム名を設定

    # nameが同じ行を取得
    name_to_match = name  # ここに検索したいnameを指定
    query = f"SELECT * FROM {table_name} WHERE user_name=?"
    cursor.execute(query, (name_to_match,))

    rows = cursor.fetchall()

    # カラムごとの合計を初期化
    column_sums = {column_name: 0 for column_name in column_names}
    
    # 取得した行を処理して合計を計算
    count = 0
    for row in rows:
        print(row)
        count += 1
        for i, column_value in enumerate(row[1:-1]):  # インデックスを使ってアクセス
           
            column_name = column_names[i]
            if column_name != 'user_name':  # user_name以外のカラムのみ処理
                column_sums[column_name] += column_value

    # 平均を計算
    if count > 0:
        average_values = {column_name: column_sums[column_name] / count for column_name in column_names if column_name != 'user_name'}  # user_nameは除外
    else:
        average_values = {column_name: 0 for column_name in column_names if column_name != 'user_name'}  # user_nameは除外

    # 平均を表示（テスト用）
    print(average_values)
    for column_name, average in average_values.items():
        print(f'Average {column_name} for {name_to_match}: {average}')
    # 平均を計算し終えたので、nameが同じ行を削除
    cursor.execute(f"DELETE FROM {table_name} WHERE user_name=?", (name_to_match,))

    # データベースへの変更をコミット
    conn.commit()
    # 接続を閉じる
    conn.close()
    return average_values
if __name__ == "__main__":
    main("./emotions.db","name")