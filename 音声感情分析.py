import requests
# https://qiita.com/keki/items/c0bea07274fe41a14978
# 音声ファイル条件
# PCM WAVE形式、16bitであること。
# データサイズが1.9MB以下であること。
# フォーマットがPCM_FLOAT、PCM_SIGNED、PCM_UNSIGNEDいずれかであること。
# 録音時間が5.0秒未満であること。
# サンプリング周波数が11025Hzであること。
# チャンネル数が1(モノラル)であること
import wave

def check_audio_file(filename):
    try:
        with wave.open(filename, 'rb') as audio_file:
            # フォーマットチェック
            # sample幅16ビット(2バイト)
            if audio_file.getsampwidth() != 2:
                return False
            # モノラル
            if audio_file.getnchannels() != 1:
                return False
            # サンプリング周波数
            if audio_file.getframerate() != 11025:
                return False

            # データサイズチェック
            audio_file_size = audio_file.getnframes() * audio_file.getsampwidth()
            if audio_file_size > 1.9 * 1024 * 1024:
                return False

            # 録音時間チェック
            recording_time = audio_file.getnframes() / audio_file.getframerate()
            if recording_time >= 5.0:
                return False
    except wave.Error:
        return False

    return True

def get_audio_file_info(filename):
    try:
        with wave.open(filename, 'rb') as audio_file:
            sample_width = audio_file.getsampwidth()
            channels = audio_file.getnchannels()
            sample_rate = audio_file.getframerate()
            frames = audio_file.getnframes()

            return {
                'sample_width': sample_width,
                'channels': channels,
                'sample_rate': sample_rate,
                'frames': frames
            }
    except wave.Error:
        return None
def main(audio_file_path):
    global emotion
    
    

    # 音声ファイルの条件チェック
    if check_audio_file(audio_file_path):
        print("音声ファイルの条件を満たしています。")
        # 音声ファイルの情報取得
        audio_file_info = get_audio_file_info(audio_file_path)
        if audio_file_info is not None:
            print("音声ファイルの情報:")
            print(f"サンプル幅: {audio_file_info['sample_width']} bytes")
            print(f"チャンネル数: {audio_file_info['channels']}")
            print(f"サンプルレート: {audio_file_info['sample_rate']} Hz")
            print(f"フレーム数: {audio_file_info['frames']}")
        else:
            print("音声ファイルの情報を取得できませんでした。")
    else:
        print("音声ファイルの条件を満たしていません。")
        emotion = error
emotion = {'error': "エラー", 'calm': "冷静", 'anger': "怒り", 'joy': "喜び", 'sorrow': "悲しみ", 'energy': "エネルギー"}
error = {'error': "エラー", 'msg': "メッセージ", 'expected':"期待"}

if __name__  == "__main__":
    
    # 音声ファイルのパス
    audio_file_path = './AISATSU_001_11025.wav'
    main(audio_file_path)
    url = 'https://api.webempath.net/v2/analyzeWav'
    apikey = 'APIKEY'
    payload = {'apikey': apikey}

    data = open(audio_file_path, 'rb')
    file = {'wav': data}


    res = requests.post(url, params=payload, files=file)
    print(res.json())
    for i in res.json():
        print(emotion[i]+":"+str(res.json()[i]))