# ライブラリのインポート
from flask import Flask, render_template, request, jsonify, session,redirect
import secrets
from pyngrok import ngrok, conf
import subprocess
from logging import FileHandler, WARNING
import base64
import os
import uuid
# 他のカスタムモジュールのインポート
from blueprint import User
from blueprint import Face
from blueprint import AIchat
from blueprint import Create_Image
from blueprint import Chat
from blueprint import Re_Set_Password

# 他のPythonプログラムのインポート
from modules import get_topic
from modules import search
from modules import ngrok_setup
from modules import ocr_program
if not os.path.isdir("static/images/create"):
    os.mkdir("static/images/create")
if not os.path.isdir("static/images/chat"):
    os.mkdir("static/images/chat")
if not os.path.isdir("static/images/ocr"):
    os.mkdir("static/images/ocr")
if not os.path.isdir("static/images/streaming"):
    os.mkdir("static/images/streaming")
# Flaskアプリケーションのインスタンス化
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # ランダムなシークレットキーを生成
app.template_folder = 'template'  # HTMLテンプレートのフォルダ設定
app.static_folder = 'static'  # 静的ファイル（CSS、JavaScriptなど）のフォルダ設定

# カスタムモジュールとBlueprintの登録
app.register_blueprint(User.bp)
app.register_blueprint(Face.face)
app.register_blueprint(AIchat.aichat)
app.register_blueprint(Create_Image.create_imgae)
app.register_blueprint(Chat.chat)
app.register_blueprint(Re_Set_Password.reset_pass)

# 設定ファイルの読み込み
app.config.from_pyfile('config.py')
F_H = FileHandler("data/errorlogs.txt")
F_H.setLevel(WARNING)
app.logger.addHandler(F_H)

# 起動時の表示
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ocr')
def ocrindex():
    return render_template('ocr.html')
@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        data = request.get_json()
        image_data = data['image_data']
        
        # データURLから画像データを取得
        _, image_data = image_data.split(',', 1)
        image_binary = base64.b64decode(image_data)
        
        # 画像を保存
        path="static/images/ocr/"+str(uuid.uuid4())+".png"
        while os.path.isfile(path):
            path="static/images/ocr/"+str(uuid.uuid4())+".png"
        
        with open(path, 'wb') as f:
            f.write(image_binary)
        text=ocr_program.main(path)
        return jsonify({"data":{'success': True,"text":text}})
    except Exception as e:
        return jsonify({"data":{'success': False, 'error': str(e)}})

@app.route('/myvideo')
def myvideo():
    if "user_id" in session:
        return render_template('video.html',id=session["user_id"])
    return redirect("/login2")
    
    
@app.route('/myvideo', methods=['POST'])
def video_write():
    if "user_id" in session:
        id = session["user_id"]
        # リクエストからデータURI形式の画像データを取得
        data_uri = request.json['frame']

        with open(f"./static/images/streaming/{id}_captured_frame.txt","w") as f:
            f.write(data_uri)
        return jsonify({'message': 'Image saved successfully'})
    return jsonify({'message': 'not lgoin'})

@app.route('/video/<int:id>')
def video_view(id):
    return render_template('videoview.html')
@app.route('/video/<int:id>', methods=['POST'])
def video_get(id):
    with open(f"./static/images/streaming/{id}_captured_frame.txt","r") as f:
        data=f.readline()
    return jsonify({"data":data})
# ファビコンの表示
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# セッションのユーザー名を取得するAPI
@app.route('/sessionusername', methods=['POST'])
def sessionusername():
    username = "None"
    for i in session:
        if i == "username":
            username = session["username"]
    sessions = {"sessionusername": username}
    return jsonify(sessions)

# 検索のAPI
@app.route('/search', methods=['POST'])
def searchs():
    result = {"arr": get_topic.main(request.json['search'])}
    return jsonify(result)

# 検索結果ページのAPI
@app.route("/search_Results_Page", methods=["POST"])
def search_Results_Page():
    result = search.main2(request.json['search'])
    return jsonify(result)

# ランキングのAPI
@app.route('/Ranking', methods=['POST'])
def Ranking():
    result = {"arr": get_topic.main()}
    return jsonify(result)

# シャットダウンのAPI
@app.route('/shutdown')
def shutdown():
    import os
    os.system('shutdown -s')
@app.route("/docs")
def pathlist():
    return render_template("docs.html", paths=show_url_paths())
# エラーハンドラー
@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    return "Internal Server Error", 500 
def show_url_paths():
    output = []
    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return output

# サーバーの起動
def startserver(port,is_debug):
    
    # print(show_url_paths())
    
    if is_debug:
        app.run(port=port,debug=True)
    else:
        print("Do you want to set the DOMAIN")
        select = input("y, n")
        if select == "y" or select == "Y":
            ngrok_setup.setup(port)
        else:
            ngrok_setup.portset(port)

        # ngrokを起動するコマンド
        ngrok_command = "ngrok start myapp"
        
        # ngrokを起動
        ngrok_process = subprocess.Popen(ngrok_command, shell=True)
        try:
            app.run(port=port)
                
        except Exception as e:
            print(e)
            ngrok_process.terminate()

if __name__ == '__main__':
    isdebug=False
    if input("debug-mode:(y・n):")=="y":
        isdebug=True
    
    startserver(5000,isdebug)
