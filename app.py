from flask import Flask, render_template, request, jsonify
import base64
import cv2
import datetime
from fer import FER
import numpy as np
import os
import json
import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # 16バイトのランダムなバイト列を16進数文字列に変換してシークレットキーに設定
app.debug = True
app.template_folder = 'template'
app.static_folder = 'static'
from login import user
import Face
app.register_blueprint(user.bp)
app.register_blueprint(Face.face)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    
    return render_template('index.html')

@app.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500
if __name__ == '__main__':
    app.run()