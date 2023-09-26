import pandas as pd

def main(path):
    # 初期のデータを作成
    initial_data = {
        'angry': None,
        'disgust': None,
        'fear': None,
        'happy': None,
        'sad': None,
        'surprise': None,
        'neutral': None
    }

    # データフレームを作成
    df = pd.DataFrame([initial_data])

    # CSVファイルに書き込む
    df.to_csv(path, index=False, header=True)  # ヘッダー行を追加
    

    # CSVファイルを読み込みます
    df = pd.read_csv(path)

    # 空白の行を削除します
    df = df.dropna(how='all')

    # CSVファイルに保存します
    df.to_csv(path, index=False)
if __name__ == "__main__":
    main("./emotions.csv")
