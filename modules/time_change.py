from datetime import datetime
def time_change(original_data):
    # フォーマットの指定
    input_format = "%Y%m%d%H%M%S"  # 入力データのフォーマット
    output_format = "%Y年%m月%d日 %H時%M分%S秒"  # 出力データのフォーマット

    # データ変換
    parsed_date = datetime.strptime(original_data, input_format)
    formatted_date = parsed_date.strftime(output_format)
    return formatted_date
print(time_change("20231004105905"))