from flask import Flask, render_template, request, jsonify,Blueprint


# インスタンス化 (変数名と文字列は同じに)
face = Blueprint("face",__name__)

# 関数と文字列の名前は同じに
@face.route('/face_emotion')
def face_emotion():
    
    return render_template('face.html')

# エラー対策
@face.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500