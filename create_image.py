from flask import Flask, render_template, request, jsonify,Blueprint
import 画像生成3
import 翻訳
# インスタンス化
create_imgae = Blueprint("create_imgae",__name__)

@create_imgae.route('/create_image_index')
def create_image_index():
    
    return render_template('create_imgae.html')

@create_imgae.errorhandler(500)
def internal_server_error(e):
    return "Internal Server Error", 500


@create_imgae.route('/image' ,methods=['POST'])
def image():
    
    result = {"img":画像生成3.main(request.json["array"]['PROMPT'],MODEL_ID=request.json["array"]["MODEL_ID"])}
    return jsonify(result)


@create_imgae.route('/translation' ,methods=['POST'])
def translation():
    result = {"txt":翻訳.main(request.json['txt'])}
    return jsonify(result)

