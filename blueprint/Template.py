from flask import Flask, render_template, request, jsonify,Blueprint


# インスタンス化 (変数名と文字列は同じに)
template = Blueprint("template",__name__)

# 関数と文字列の名前は同じに
@template.route('/')
def face_emotion():
    
    return render_template('index.html')
# フォームからの関数
@template.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        return "postを受け取りました"
    elif request.method == 'GET':
        return "getを受け取りました"
# エラー対策
@template.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500


