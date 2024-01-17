# ライブラリのインポート
from flask import Flask, render_template, request, jsonify, session,redirect
from flask_cors import CORS
from flask_socketio import emit, SocketIO, join_room,leave_room
import secrets
from pyngrok import ngrok, conf
import subprocess
from logging import FileHandler, WARNING
import base64
import os
import uuid
# Flaskアプリケーションのインスタンス化
app = Flask(__name__)
CORS(app, resources={r"/socket.io/*": {"origins": "*"}})

app.secret_key = secrets.token_hex(16)  # ランダムなシークレットキーを生成
app.template_folder = 'template'  # HTMLテンプレートのフォルダ設定
app.static_folder = 'static'  # 静的ファイル（CSS、JavaScriptなど）のフォルダ設定
sio  = SocketIO(app, async_mode='threading') 
# 他のPythonプログラムのインポート
from modules import get_topic
from modules import search
from modules import ngrok_setup
from modules import globaldata
globaldata.Global.SocketIO=sio
# 他のカスタムモジュールのインポート
from blueprint import User
from blueprint import Face
from blueprint import AIchat
from blueprint import Create_Image
from blueprint import Chat_ve
from blueprint import Re_Set_Password
sio=globaldata.Global.SocketIO

if not os.path.isdir("static/images/create"):
    os.mkdir("static/images/create")
if not os.path.isdir("static/images/chat"):
    os.mkdir("static/images/chat")
if not os.path.isdir("static/images/streaming"):
    os.mkdir("static/images/streaming")




# カスタムモジュールとBlueprintの登録
app.register_blueprint(User.bp)
app.register_blueprint(Face.face)
app.register_blueprint(AIchat.aichat)
app.register_blueprint(Create_Image.create_imgae)
app.register_blueprint(Chat_ve.chat)
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

@app.route('/myvideo')
def myvideo():
    if "user_id" in session:
        return render_template('video.html',id=session["user_id"])
    return redirect("/login2")
    
    
@sio.on('stopvideo')
def stopvideo(data):
    if "user_id" in session:
        id = session["user_id"]
        # リクエストからデータURI形式の画像データを取得
        
        data_uri = data_uri = "../static/images/road_image.jpg"
        
        url = "stopvideo"+str(id)
        
        emit(url,data_uri,broadcast=True)
@sio.on('video')
def video(data):
    
    if "user_id" in session:
        id = session["user_id"]
        # リクエストからデータURI形式の画像データを取得
        
        data_uri = data['frame']
        
        if data["password"]=="null":
            url = "videoid"+str(id)
        else:
            url = "videoid"+str(id)+"pass"+data["password"]
        emit(url,data_uri,broadcast=True)
@sio.on('viewstart')
def viewstart(data):
    
    emit("viewstart"+str(data["id"]),"",broadcast=True)
@sio.on('viewend')
def viewend(data):
    
    emit("viewend"+str(data["id"]),"",broadcast=True)
@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")
@app.route('/video/<int:id>')
def video_view(id):
    return render_template('videoview.html',id=id)

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
from modules import google_translation
@app.route('/translationtxt' ,methods=['POST'])
def translation():
    data = request.get_json()
    print(data)
    result=google_translation.translation(data['txt'],data['dest'])
    return jsonify({"result":result})
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
        
        sio.run(app,port=port,debug=True)
    else:
        print("Do you want to set the DOMAIN")
        select = input("y, n")
        if select == "y" or select == "Y":
            ngrok_setup.setup(port)
        else:
            ngrok_setup.portset(port)

        # ngrokを起動するコマンド
        ngrok_command = "ngrok start ITalk"
        
        # ngrokを起動
        ngrok_process = subprocess.Popen(ngrok_command, shell=True)
        try:
            sio.run(app,port=port)
            
                
        except Exception as e:
            print(e)
            ngrok_process.terminate()
import sys
# サーバーの起動
def start(port):
    
    conf.get_default().auth_token = sys.argv[2]
    
    public_url = ngrok.connect(port,hostname=sys.argv[3])
    print(f"ngrok URL: {public_url}")
    sio.run(app,port=port)
if __name__ == '__main__':
    # start(sys.argv[1])?
    start(sys.argv[1])

