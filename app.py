from flask import Flask, render_template, request, jsonify
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
# 他のインスタンス化したものを追加
app.register_blueprint(user.bp)
app.register_blueprint(Face.face)
app.register_blueprint(AIchat.aichat)
app.register_blueprint(create_image.create_imgae)
# configファイル設定
app.config.from_pyfile('config.py')

# 起動時の表示
@app.route('/')
def index():
    
    return render_template('index.html')

import トピック取得

@app.route('/search' ,methods=['POST'])
def search():
    result = {"arr":トピック取得.main(request.json['search'])}
    return jsonify(result)

import 検索
@app.route("/search_Results_Page",methods=["POST"])
def search_Results_Page():
    result = 検索.main(request.json['search'])
    print(result)
    return jsonify(result)


@app.route('/Ranking' ,methods=['POST'])
def Ranking():
    
    result = {"arr":トピック取得.main()}
    print(result)
    return jsonify(result)

# エラー対策
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

if __name__ == '__main__':
    is_upload=input("0:非公開,1:公開")
    
    if is_upload =="0" :
        app.run()
    elif is_upload =="1":
        app.run(host='0.0.0.0')
    else:
        print("設定されていません")
    