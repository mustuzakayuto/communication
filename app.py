from flask import Flask, render_template, request, jsonify ,session
import secrets
import sys

# メインのFlaskをインスタンス化
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 16バイトのランダムなバイト列を16進数文字列に変換してシークレットキーに設定
# app.debug = True
# htmlのフォルダー設定
app.template_folder = 'template'
# staticフォルダー設定
app.static_folder = 'static'
from login import user

import Face
import AIchat 
import create_image
import chat
import re_set_password
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

@app.route('/sessionusername' ,methods=['POST'])
def sessionusername():
    username="None"
    for i in session:
        if i == "username":
            username=session["username"]
    sessions = {"sessionusername":username}
    return jsonify(sessions)
import get_topic

@app.route('/search' ,methods=['POST'])
def search():
    result = {"arr":get_topic.main(request.json['search'])}
    return jsonify(result)

import search
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

if __name__ == '__main__':
    app.run()
    # is_upload=input("-1:デバック,0:公開,1:https公開")
    # if is_upload=="-1":
    #     app.run(debug=True)
    # elif is_upload =="0" :
    #     app.run(host='0.0.0.0')
    # elif is_upload =="1":
    #     import ssl
    #     context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #     context.load_cert_chain('openssl/server.crt', 'openssl/server.key')
    #     app.run(host='0.0.0.0',ssl_context=context)
    
    # else:
    #     print("設定されていません")
    