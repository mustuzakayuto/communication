from flask import Flask, render_template, request, jsonify ,session
import secrets
from pyngrok import ngrok, conf
import subprocess 


from login import user
import Face
import AIchat 
import create_image
import chat
import re_set_password

import get_topic
import search
import ngrok_setup



# メインのFlaskをインスタンス化
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 16バイトのランダムなバイト列を16進数文字列に変換してシークレットキーに設定
# app.debug = True
# htmlのフォルダー設定
app.template_folder = 'template'
# staticフォルダー設定
app.static_folder = 'static'

# 他のインスタンス化したものを追加
app.register_blueprint(user.bp)
app.register_blueprint(Face.face)
app.register_blueprint(AIchat.aichat)
app.register_blueprint(create_image.create_imgae)
app.register_blueprint(chat.chat)
app.register_blueprint(re_set_password.reset_pass)
# configファイル設定
app.config.from_pyfile('config.py')

# 起動時の表示
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')
@app.route('/sessionusername' ,methods=['POST'])
def sessionusername():
    username="None"
    for i in session:
        if i == "username":
            username=session["username"]
    sessions = {"sessionusername":username}
    return jsonify(sessions)


@app.route('/search' ,methods=['POST'])
def searchs():
    result = {"arr":get_topic.main(request.json['search'])}
    return jsonify(result)


@app.route("/search_Results_Page",methods=["POST"])
def search_Results_Page():
    result = search.main(request.json['search'])
    print(result)
    return jsonify(result)


@app.route('/Ranking' ,methods=['POST'])
def Ranking():
    
    result = {"arr":get_topic.main()}
    # print(result)
    return jsonify(result)

# エラー対策
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

    

def startserver(port):
    print("Do you want to set the DOMAIN")
    select=input("y,n")
    if select =="y" or select=="Y":
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
    
    startserver(5000)