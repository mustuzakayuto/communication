import base64
from PIL import Image
from io import BytesIO
def main(base64_image,name):
    image_data = base64.b64decode(base64_image.split(',')[1])

    # Pillowを使用して画像を開く
    image = Image.open(BytesIO(image_data))

    # 画像をファイルに保存
    image.save(name)