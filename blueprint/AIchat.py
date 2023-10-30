# 必要なライブラリのインポート
from flask import Flask, render_template, request, jsonify, Blueprint, session, redirect
import requests
import os
import json

# APIエンドポイントのURLとヘッダー設定
url = "https://api-mebo.dev/api"
headers = {'content-type': 'application/json'}

# config.json ファイルのパスを設定
if os.path.isfile("../config.json"):
    config_path = ".."
else:
    config_path = "."

# ITALKエージェントの設定 (config.json ファイルから取得)
config_file = open(config_path + "/config.json", "r")
config_data = json.load(config_file)
api_key = config_data["agent"]["key"]
agent_id = config_data["agent"]["id"]

# ブループリント（Blueprint）のインスタンス化
aichat = Blueprint("aichat", __name__)

# チャット画面表示用のルート
@aichat.route('/chat_index')
def chat_index():
    # セッションにユーザーが存在するか確認
    if "username" in session:
        return render_template('ai_chat.html')
    else:
        # ユーザーがログインしていない場合はログインページにリダイレクト
        return redirect("/login")

# エラーハンドラー
@aichat.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

# チャットフォームからのリクエストを処理
@aichat.route('/chat', methods=('GET', 'POST'))
def chat():
    if request.method == 'POST':
        inputdata = request.json['inputdata']
        if inputdata == "":
            return jsonify({"result": "質問に文字を入れてください"})
        
        item_data = {
            "api_key": api_key,
            "agent_id": agent_id,
            "utterance": inputdata,
            "uid": "ユーザ識別子"
        }

        # チャットボットAPIにリクエストを送信
        r = requests.post(url, json=item_data, headers=headers)
        
        # レスポンスを取得し、回答を抽出
        result = "回答: " + r.json()["bestResponse"]["utterance"]
        return jsonify({"result": result})
    
    elif request.method == 'GET':
        return "GETリクエストを受け取りました"
