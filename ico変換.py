from PIL import Image
def main():
    static="static/"
    # PNG画像　ファイル名
    # PNG_FILE_NAME = static+"sample.jpg"
    PNG_FILE_NAME = static+input("ファイルネーム(拡張子必須):")
    # ICO画像　ファイル名
    ICO_FILE_NAME = static+"sample.ico"
    
    # PNG画像を開く
    img = Image.open(PNG_FILE_NAME)
    
    # ICO画像保存
    img.save(ICO_FILE_NAME, format="ICO", sizes=[(132, 132)])
if __name__ =="__main__":
    main()