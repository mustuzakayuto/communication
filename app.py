from flask import Flask, render_template, request, jsonify
import base64
import cv2
import datetime
from fer import FER
import numpy as np
import os
import json
import secrets
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
# 他のインスタンス化したものを追加
app.register_blueprint(user.bp)
app.register_blueprint(Face.face)
app.register_blueprint(AIchat.aichat)
# configファイル設定
app.config.from_pyfile('config.py')

# 起動時の表示
@app.route('/')
def index():
    
    return render_template('index.html')

# エラー対策
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000)
    