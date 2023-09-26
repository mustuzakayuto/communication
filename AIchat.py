from flask import Flask, render_template, request, jsonify,Blueprint ,session
import requests
import os
import json
url = "https://api-mebo.dev/api"
headers = {'content-type': 'application/json'}
# miiboの設定(api)
# api_key = "api_key"
# agent_id = "agent_id"



if os.path.isfile("../config.json"):
    tag=".."
else:
    tag="."
tag="."
# ITALKエージェントを設定


json_open = open(tag+"/config.json","r")
json_load = json.load(json_open)
api_key = json_load["agent"]["key"]
agent_id = json_load["agent"]["id"]
# インスタンス化 (変数名と文字列は同じに)
aichat = Blueprint("aichat",__name__)

# 関数と文字列の名前は同じに
@aichat.route('/chat_index')
def chat_index():
    return render_template('ai_chat.html')

# エラー対策
@aichat.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

# フォームからの関数
@aichat.route('/chat', methods=('GET', 'POST'))
def chat():
    if request.method == 'POST':
        inputdata = request.json['inputdata']
        if inputdata =="":
            return jsonify({"result":"質問に文字を入れてください"})
        
        item_data = {
            "api_key": api_key,
            "agent_id": agent_id,
            "utterance": inputdata,
            "uid": "ユーザ識別子"
        }
        print(item_data)
        r = requests.post(url,json=item_data,headers=headers)
        print(r)
        print(agent_id,api_key)
        result = "回答: "+r.json()["bestResponse"]["utterance"]
        return jsonify({"result":result})
    elif request.method == 'GET':
        return "getを受け取りました"
