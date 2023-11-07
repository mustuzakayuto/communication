from flask import Flask, render_template, request, jsonify,Blueprint, session, redirect,send_file
from modules import create_image3
from modules import google_translation
from modules import time_change

import time
import config
import sqlite3
import uuid

# インスタンス化
create_imgae = Blueprint("create_imgae",__name__)
joblist=[]
class Job:
    def __init__(self) :
        self.setid()
    def setid(self):
        self.id=uuid.uuid4()
        while self.id in joblist:
            self.id=uuid.uuid4()
        joblist.append(self.id)

@create_imgae.route('/create_image_index')
def create_image_index():
    if "username" in session:
        return render_template('create_imgae.html')
    else :
        return redirect("/login")

    
@create_imgae.errorhandler(500)
def internal_server_error(e):

    return "Internal Server Error", 500
@create_imgae.route('/imagelog')
def imagelogindex():
    return render_template('image_log.html')
@create_imgae.route('/imagelog' ,methods=['POST'])
def imagelog():
    username = session['username']
    imgs=get(username,"img")
    times=get(username,"time")
    # for img in imgs:
    #     times.append(time_change.time_change(img.split("create/")[1].split(".")[0].split("_")[1]))
    prompts=get(username,"prompt")
    
    
    result={"arr":{"img_list":imgs,"times":times,"prompt":prompts}}
    return jsonify(result)

@create_imgae.route('/download_img' ,methods=['POST'])
def download_img():
    downloadFileName = request.json['imgname']
    png_file_path = 'static/images/create/' + downloadFileName
    
    # ファイルをダウンロードとして提供
    return send_file(png_file_path, as_attachment=True)

        
@create_imgae.route('/image' ,methods=['POST'])
def image():
    prompt = request.json["array"]['PROMPT']
    model_id = request.json["array"]["MODEL_ID"]
    
    
    # タスクをキューに追加
    # job = q.enqueue(create_image3.main, prompt, model_id)
    job = Job()
    while joblist[0]!=job.id:
        time.sleep(1)
    imagepath,timedata=create_image3.main(request.json["array"]['PROMPT'],MODEL_ID=request.json["array"]["MODEL_ID"])
    username = session['username']
    result = {"img":imagepath}
    addimage(imagepath,username,prompt,timedata)
    joblist.pop(0)
    return jsonify(result)
@create_imgae.route('/job_status')
def get_job_status():
    
    print(joblist)
    return jsonify({"joblist":joblist})

@create_imgae.route('/entranslation' ,methods=['POST'])
def entranslation():
    result = {"txt":google_translation.main(request.json['txt'])}
    return jsonify(result)

def addimage(image_name,user_name,prompt,timedata):
    conn = sqlite3.connect(config.IMAGEDATABASE)

    # カーソルを取得
    cursor = conn.cursor()

    # data入れる
    cursor.execute(f'''INSERT INTO images (image_name, user_name,prompt,time)
    VALUES (?, ?,?,?);
    ''', (image_name,user_name,prompt,timedata))  # プレースホルダーを使って値を挿入
    # 変更をコミット
    conn.commit()

    # 接続を閉じる
    conn.close()
def get(user_name,gettype):
    if gettype=="img":
        gettype=1
    elif gettype=="prompt":
        gettype=3
    elif gettype=="time":
        gettype=4
    # データベースに接続
    conn = sqlite3.connect(config.IMAGEDATABASE)

    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリを実行
    cursor.execute("SELECT * FROM images  WHERE user_name=?", (user_name,))

    # 結果を取得
    data = cursor.fetchall()
    # print(data)
    imagelist=[]
    # データを処理
    for row in data:
        imagelist.append(row[gettype])

    # データベース接続を閉じる
    conn.close()
    return imagelist