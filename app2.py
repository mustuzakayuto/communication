# ライブラリのインポート
from flask import Flask, render_template, request, jsonify, session
import secrets
from pyngrok import ngrok, conf
import subprocess
from logging import FileHandler, WARNING
import os

# 他のカスタムモジュールのインポート
from blueprint import User
from blueprint import Face2
from blueprint import AIchat
from blueprint import Create_Image
from blueprint import Chat
from blueprint import Re_Set_Password

# 他のPythonプログラムのインポート
from modules import get_topic
from modules import search

if not os.path.isdir("static/images/create"):
    os.mkdir("static/images/create")
if not os.path.isdir("static/images/chat"):
    os.mkdir("static/images/chat")

    


# Flaskアプリケーションのインスタンス化
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # ランダムなシークレットキーを生成
app.template_folder = 'template'  # HTMLテンプレートのフォルダ設定
app.static_folder = 'static'  # 静的ファイル（CSS、JavaScriptなど）のフォルダ設定

# カスタムモジュールとBlueprintの登録
app.register_blueprint(User.bp)
app.register_blueprint(Face2.face)
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
import sys
# サーバーの起動
def startserver(port):
    
    conf.get_default().auth_token = sys.argv[2]
    
    public_url = ngrok.connect(port,hostname=sys.argv[3])
    print(f"ngrok URL: {public_url}")
    app.run(port=port)
    

if __name__ == '__main__':
    # app2.py port token hostname
    startserver(sys.argv[1])
