# 必要なライブラリをインポート
from contextlib import _RedirectStream
from flask import *
import sqlite3
import config
import hashlib
import datetime
import os
import re
import uuid
import base64
from flask_socketio import emit, SocketIO, join_room,leave_room
from modules import database
from modules import google_translation
from modules import globaldata

# サポートする国のリスト
country = ["None", "en", "ja", "es", "pt", "de", "fr", "it", "ru", "ar", "tr", "ko",
           "zh-CN", "zh-TW", "hi", "bn", "uk", "el", "nl", "cs", "pl", "th", "sv", "ro", "fi", "no",
           "da", "hr", "id", "tl", "vi"]

# ブループリント（Blueprint）のインスタンス化
chat = Blueprint("chat", __name__)
chat_data_base = config.CHATDATABASE

# パスワードをハッシュ化する関数
def cash(password):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return password

# ログイン画面表示
@chat.route("/login2")
def login_get():
    if "user_id" in session:
        return render_template("set_nickname.html",username=session["user_name"])
    return render_template("login2.html")

# ユーザーリストを表示
@chat.route("/userlist2")
def userlist():
    users = []

    if "user_id" in session:
        my_id = session["user_id"]
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("SELECT id, nickname FROM user WHERE id != ?", (my_id,))
        user_info = c.fetchall()
        

        return render_template("userlist2.html", tpl_user_info=user_info)
    return redirect("/login2")

# チャットルーム作成または選択
@chat.route("/chatroom/<int:other_id>", methods=["POST"])
def chatroom_post(other_id):
    if "user_id" in session:
        my_id = session["user_id"]
        print(my_id)
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
        chat_id = c.fetchone()
        print(chat_id)

        if chat_id == None and my_id != other_id:
            c.execute("select nickname from user where id = ?", (my_id,))
            myname = c.fetchone()[0]
            c.execute("select nickname from user where id = ?", (other_id,))
            othername = c.fetchone()[0]

            room = myname + "と" + othername + "のチャット"
            c.execute("insert into chat values(null,?,?,?,0)", (my_id, other_id, room))
            conn.commit()
            c.execute("select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
            chat_id = c.fetchone()

        
        print(chat_id)
        return redirect("/chat/{}".format(chat_id[0]))
        
    else:
        return redirect("/login2")

# 自分のチャットルーム一覧を表示
@chat.route("/chatroom")
def chatroom_get():
    if "user_id" in session:
        my_id = session["user_id"]
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("select id, room from chat where user_id1 = ? or user_id2 = ? or user_id1 = ? or user_id2 = ?", (my_id, my_id, 0, 0))
        chat_list = c.fetchall()
        print(chat_list)
        return render_template("/chatroom2.html", tpl_chat_list=chat_list)
    else:
        return redirect("/login2")

# セッション情報を取得
@chat.route("/get_session", methods=["POST"])
def get_session():
    print(session)

    if "country" in session:
        countrydata = session["country"]
        result = {"country": countrydata}
    else:
        result = {"country": "None"}
    return jsonify(result)

# セッション情報を設定
@chat.route("/session", methods=["POST"])
def set_session():
    if request.json["country"] in country:
        session["country"] = request.json["country"]
        status = {"status": "201"}
        print(session["country"])
    else:
        status = {"status": "409"}

    print(status)
    return jsonify(status)

# チャットメッセージを翻訳
@chat.route("/translation/chat/<int:chatid>", methods=["POST"])
def translation(chatid):
    message = request.json["data"]["txt"]
    chatdata = getchat(request.json["data"]["id"], chatid)

    if not "country" in session:
        session["country"] = "None"

    if session["country"] != "None" and str(chatdata).strip() != "":
        message = google_translation.translation(chatdata, session["country"])
    elif session["country"] == "None":
        message = chatdata

    result = {"txt": message}
    return jsonify(result)

def getchat(index,chatid):
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    c.execute(
        "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
    chat_fetch = c.fetchall()
   
    return chat_fetch[int(index)][2]
# チャットリスト取得
@chat.route("/get_chat_list/chat/<int:chatid>", methods=['POST'])
def get_chat_list(chatid):
    
    if "user_id" in session:
        session["chatid"]=chatid
        my_id = session["user_id"]
        if not "country" in session :
            session["country"]="None"
        print(session["country"])
        # ここにチャットをDBからとって、表示するプログラム
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute(
            "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name ,chatmess.time,chatmess.type from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
        chat_fetch = c.fetchall()
        chat_info = []
        for chat in chat_fetch:
            message=chat[2]
            if request.json["is_road"]=="true":
                
                if session["country"]!="None" and str(chat[2]).strip()!="" and chat[5]=="text":
                    message=google_translation.translation(chat[2],session["country"])
            chat_info.append(
                {"to": chat[0], "from": chat[1], "message": message, "fromname": chat[3],"time":chat[4],"type":chat[5]}
                )

        c.execute("select room from chat where id = ?", (chatid,))
        room_name = c.fetchone()[0]
        
        result={"data":{"chat_list":chat_info,"my_id":my_id,"type":session["country"],"len":len(chat_info)}}
        return jsonify(result)

    
# チャットルーム表示
@chat.route("/chat/<int:chatid>")
def chat_get(chatid):
    if "user_id" in session:
        my_id = session["user_id"]
        # ここにチャットをDBからとって、表示するプログラム
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("select user_id1, user_id2 from chat where id = ?", (chatid,))
        userids = c.fetchall()[0]
        if not my_id in userids and not 0 in userids:
            return redirect("/userlist2")
        
        c.execute(
            "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
        chat_fetch = c.fetchall()
        chat_info = []
        for chat in chat_fetch:
            chat_info.append(
                {"to": chat[0], "from": chat[1], "message": chat[2], "fromname": chat[3]})

        c.execute("select room from chat where id = ?", (chatid,))
        room_name = c.fetchone()[0]
        
        return render_template("chat2.html", chat_list=chat_info, link_chatid=chatid, tpl_room_name=room_name, tpl_my_id=my_id)
    else:
        return redirect("/login2")

@globaldata.Global.SocketIO.on('chatupload')
def chatupload(data):
    if "user_id" in session:
        # ここにチャットの送信ボタンが押されたときにDBに格納するプログラム
        my_id = session["user_id"]
        current_time = datetime.datetime.now()
        time= current_time.strftime("%m/%d,%I:%M %p")
        print(data)
        chat_message = data["chattext"]
        chatid=int(data["chatid"])
        
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute(
            "select user_id1, user_id2 from chat where id = ?", (chatid,))
        chat_user = c.fetchone()
        print(chat_user)
        if my_id != chat_user[0]:
            to_id = chat_user[0]
        else:
            to_id = chat_user[1]
        print(to_id)
        if str(chat_message).strip()=="":
            return redirect("/chat/{}".format(chatid))
        c.execute("insert into chatmess values(null,?,?,?,?,?,?)",
                  (chatid, to_id, my_id, chat_message,time,"text",))
        conn.commit()
        
        
        emit("updateid"+str(chatid),"upload",broadcast=True)
        return render_template("/chat/{}".format(chatid))
    else:
        return redirect("/login2")

@globaldata.Global.SocketIO.on('chatimageupload')
def chatupload(data):
    imagelist = ['png', 'jpg', 'jpeg', 'gif']

    file_data_url = data["fileDataUrl"]
    chatid = data["chatid"]

    # Extract file extension from the data URL
    file_extension = file_data_url.split(';')[0].split('/')[1]

    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])

    if file_extension in allowed_extensions:
        if file_extension in imagelist:
            datatype = "img"
        elif "mp4" == file_extension:
            datatype = "video"

        # Decode the base64 data URL to get the binary data
        try:
            file_data = base64.b64decode(file_data_url.split(',')[1])
        except Exception as e:
            print("Error decoding base64:", e)
            return redirect("/chat/{}".format(chatid))

        # Generate a unique filename
        hashfilename = str(hashlib.sha256(str(chatid).encode("utf-8")).hexdigest())
        filename = hashfilename + str(uuid.uuid4()) + "." + file_extension

        try:
            with open(os.path.join('./static/images/chat', filename), 'wb') as f:
                f.write(file_data)
            
        except Exception as e:
            print("Error saving file:", e)
            return redirect("/chat/{}".format(chatid))

        current_time = datetime.datetime.now()
        time = current_time.strftime("%m/%d,%I:%M %p")

        my_id = session["user_id"]
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("select user_id1, user_id2 from chat where id = ?", (chatid,))
        chat_user = c.fetchone()

        if my_id != chat_user[0]:
            to_id = chat_user[0]
        else:
            to_id = chat_user[1]

        chat_message="../static/images/chat/"+filename
        c.execute("insert into chatmess values(null,?,?,?,?,?,?)",
                  (chatid, to_id, my_id, chat_message, time, datatype,))
        conn.commit()
        emit("updateid"+str(chatid),"upload",broadcast=True)

        return redirect("/chat/{}".format(chatid))

    else:
        return redirect("/chat/{}".format(chatid))


# ログインするプログラム。
@chat.route("/login2", methods=["POST"])
def login():
    name = request.form.get("username")
    password = request.form.get("password")
    
    if name==""or password=="":
        return render_template("login2.html",error="文字列を入力してください")
    password = cash(password)
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    c.execute(
        "select id,nickname from user where name = ? and password = ?", (name, password,))
    user_id = c.fetchone()
    
    
    if user_id is None:
        return render_template("login2.html",error="アカウントが存在しません")
    else:
        session['user_id'] = user_id[0]
        session["user_name"]=user_id[1]
        return redirect("/userlist2")
    
    
# ニックネーム変更プログラム。
@chat.route("/set_nickname", methods=["POST"])
def set_nickname():
    if "user_id" in session:
        nickname= request.form.get("nickname")
        userid=session['user_id']
        if nickname=="":
            return render_template("set_nickname.html",username=session["user_name"],error="文字列を入力してください")
        special_characters_pattern = r'[!@#$%^&*()_+{\[\]:;<>,.?~\\|/-]'
        if re.search(special_characters_pattern,nickname):
            return render_template("set_nickname.html",username=session["user_name"],error="特殊文字を入力しないでください")
        
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("UPDATE user SET nickname = ? WHERE id = ?", (nickname,userid, ))
        conn.commit()
        session["user_name"]=nickname
    else:
         return render_template("set_nickname.html",error="ログインしてください")
    return render_template("set_nickname.html",username=session["user_name"])

# アカウント作成(新規ユーザー登録)プログラム
@chat.route("/regist", methods=["POST"])
def regist():
    name = request.form.get("username")
    password = request.form.get("password")
    useremail = request.form.get("email")
    if name==""or password=="":
        return render_template("login2.html",error="文字列を入力してください")
    special_characters_pattern = r'[!@#$%^&*()_+{\[\]:;<>,.?~\\|/-]'
    if re.search(special_characters_pattern, name) or re.search(special_characters_pattern, password):
        return render_template("login2.html",error="特殊文字を入力しないでください")
    password = cash(password)
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    # 同じ名前のユーザーが既に存在するか確認
    c.execute("SELECT id FROM user WHERE name = ?", (name,))
    existing_user = c.fetchone()
    

    # 既存のユーザーが存在する場合
    if existing_user:
        return render_template("login2.html",error="アカウントが存在します")
    
    else:
        c.execute("insert into user values(null,?,?,?)", (name, password,name,))
        conn.commit()
    
    return redirect("/login2")

# ログアウト
@chat.route("/logout2")
def logout():
    if "user_id" in session:
        session.pop("user_id", None)
        return redirect("/login2")
    
    return redirect("/login2")
        

