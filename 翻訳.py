from googletrans import LANGUAGES, Translator

def main(text):
    translator = Translator()
    detected_lang = translator.detect(text).lang

    # 言語が正しく検出できなかった場合に備えて、デフォルトの言語名を設定
    detected_lang_name = LANGUAGES.get(detected_lang, "言語が検出できませんでした")

    # 言語が正しく検出された場合のみ翻訳を実行
    if detected_lang != 'unknown':
        translated = translator.translate(text, src=detected_lang, dest='en').text
        print("検出言語: " + detected_lang_name)
        print("英語語訳: " + translated)
        return translated
    else:
        print("言語の検出に失敗しました。")
        return "言語の検出に失敗しました。"

# translated_text = main("黑兔")
# print("翻訳結果:", translated_text)
