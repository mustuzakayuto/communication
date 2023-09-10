from flask import Flask, render_template, request, jsonify,Blueprint

# インスタンス化
create_imgae = Blueprint("create_imgae",__name__)

@create_imgae.route('/create_image_index')
def create_image_index():
    
    return render_template('create_imgae.html')

@create_imgae.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500

import 画像生成3
@create_imgae.route('/image' ,methods=['POST'])
def image():
    
    result = {"img":画像生成3.main(request.json['PROMPT'])}
    return jsonify(result)

import 翻訳
@create_imgae.route('/translation' ,methods=['POST'])
def translation():
    result = {"txt":翻訳.main(request.json['txt'])}
    return jsonify(result)

