# ocr_card.py
import os
from PIL import Image
import pyocr
import pyocr.builders

# 1.インストール済みのTesseractのパスを通す
# path_tesseract = r"C:\Users\220063\AppData\Local\Programs\Tesseract-OCR"
path_tesseract=os.getcwd()+"\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract
for i in os.environ["PATH"].split(os.pathsep):
    print(i)

def main(img_path,lang="jpn"):
    # 2.OCRエンジンの取得
    tools = pyocr.get_available_tools()
    print(tools)
    tool = tools[0]

    # 3.原稿画像の読み込み
    # img_org = Image.open("./test.png")
    img_org = Image.open(img_path)

    # 4.ＯＣＲ実行
    builder = pyocr.builders.TextBuilder()
    result = tool.image_to_string(img_org, lang=lang, builder=builder)

    # print(result)
    return result
