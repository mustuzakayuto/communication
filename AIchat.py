from flask import Flask, render_template, request, jsonify,Blueprint ,session
import requests
url = "https://api-mebo.dev/api"
headers = {'content-type': 'application/json'}
# miiboの設定(api)
# api_key = "api_key"
# agent_id = "agent_id"

# ITALKエージェントを設定
with open('../agent.txt', 'r',encoding="utf-8") as f:
    api_key = f.readline().strip()
    agent_id = f.readline().strip()
    

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
        result = "回答: "+r.json()["bestResponse"]["utterance"]
        return jsonify({"result":result})
    elif request.method == 'GET':
        return "getを受け取りました"
