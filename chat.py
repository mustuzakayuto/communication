from flask import *   # Flaskのなかみを全部持ってくる
import sqlite3  # sqliteつかいます
import config
import hashlib
import google_translation
import datetime
import os
import re

country=["None","en","ja","es","pt","de","fr",
    "it","ru","ar","tr","ko",
    "zh-CN","zh-TW",
    "hi","bn","uk","el","nl","cs",
    "pl","th","sv","ro","fi","no",
    "da","hr","id","tl","vi"]

chat=Blueprint("chat",__name__)
chat_data_base = config.CHATDATABASE


conn = sqlite3.connect(chat_data_base)
c = conn.cursor()
# ここにチャットルーム一覧をDBからとって、表示するプログラム
c.execute(
    "select id, room from chat")
chat_list=[[0,None]]
# print(c.fetchall())

for id,room in (c.fetchall()):
    
    chat_list.append([[id,room]])
    print([[id,room]])
print(chat_list)

c.execute(
    "select chat_id,message from chatmess")
print(len(chat_list))
for chat_id,message in (c.fetchall()):
    print(chat_id)
    chat_list[chat_id].append(message)
print(len(chat_list[1])-1)
def cash(password):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return password
@chat.route("/celchat")
def jump():
    return redirect("/login2")


# ユーザーを全て表示
@chat.route("/userlist2")
def userlist():
    users=[]
    if "user_id" in session:
        my_id = session["user_id"]
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute("SELECT id, name FROM user WHERE id != ?", (my_id,))
        user_info = c.fetchall()
        
        conn.close()
        
        return render_template("userlist2.html", tpl_user_info=user_info)
    return redirect("/login2")


# /userlist2で「チャットする」ボタンを押したときに動くプログラム。チャットルームがなければ(まだチャットしたことのない相手であれば)新規作成。
@chat.route("/chatroom/<int:other_id>", methods=["POST"])
def chatroom_post(other_id):
    if "user_id" in session:
        # まずはチャットルームがあるかchatidをとってくる
        my_id = session["user_id"]
        print(my_id)
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        c.execute(
            "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
        chat_id = c.fetchone()

        print(chat_id)
        # とってきたidの中身で判定。idがNoneであれば作成、それ以外(数字が入っていれば)スルー
        if chat_id == None and my_id != other_id:

            c.execute("select name from user where id = ?", (my_id,))
            myname = c.fetchone()[0]
            c.execute("select name from user where id = ?", (other_id,))
            othername = c.fetchone()[0]
            # ルーム名を作る
            room = myname + "と" + othername + "のチャット"
            c.execute("insert into chat values(null,?,?,?)",
                      (my_id, other_id, room))
            conn.commit()
            # 作ったチャットルームのidを取得
            c.execute(
                "select id from chat where (user_id1 = ? and user_id2 = ?) or (user_id1 = ? and user_id2 = ?)", (my_id, other_id, other_id, my_id))
            chat_id = c.fetchone()
        conn.close()
        print(chat_id)
        return redirect("/chat/{}".format(chat_id[0]))
    else:
        return redirect("/login2")


# 自分のチャットルーム一覧を表示するプログラム
@chat.route("/chatroom")
def chatroom_get():
    if "user_id" in session:
        my_id = session["user_id"]
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
        # ここにチャットルーム一覧をDBからとって、表示するプログラム
        c.execute(
            "select id, room from chat where user_id1 = ? or user_id2 = ?", (0, 0))
        chat_list=c.fetchall()
            
            
        c.execute(
            "select id, room from chat where user_id1 = ? or user_id2 = ?", (my_id, my_id))
        for chat in c.fetchall():
            chat_list.append(chat)
        
        
        
        print(chat_list)
        return render_template("/chatroom2.html", tpl_chat_list=chat_list)
    else:
        return redirect("/login2")
    

@chat.route("/get_session", methods=['POST'])
def get_session():
    print(session)
    if "country" in session:
        countrydata=session["country"]
        result={"country":countrydata}
    else:
        result={"country":"None"}
    return jsonify(result)
@chat.route("/session", methods=['POST'])
def set_session():
    
    if request.json["country"] in country:
        session["country"]=request.json["country"]
        status={"status":"201"}
        print(session["country"])
    else:
        status={"status":"409"}
    
    print(status)
    return jsonify(status)
@chat.route("/translation/chat/<int:chatid>", methods=['POST'])
def translation(chatid):
    message=request.json["data"]["txt"]
    chatdata=getchat(request.json["data"]["id"],chatid)
    if not "country" in session :
        session["country"]="None"
    if session["country"]!="None" and str(chatdata).strip()!="" :
    
        message=google_translation.translation(chatdata,session["country"])
    elif session["country"]=="None":
        message=chatdata
        
    result={"txt":message}
    return jsonify(result)
def getchat(index,chatid):
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    c.execute(
        "select chatmess.to_user, chatmess.from_user, chatmess.message, user.name from chatmess inner join user on chatmess.from_user = user.id where chat_id = ?", (chatid,))
    chat_fetch = c.fetchall()
   
    return chat_fetch[int(index)][2]

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
                
                if session["country"]!="None" and str(chat[2]).strip()!="":
                    message=google_translation.translation(chat[2],session["country"])
            chat_info.append(
                {"to": chat[0], "from": chat[1], "message": message, "fromname": chat[3],"time":chat[4],"type":chat[5]}
                )

        c.execute("select room from chat where id = ?", (chatid,))
        room_name = c.fetchone()[0]
        c.close()
        result={"data":{"chat_list":chat_info,"my_id":my_id,"type":session["country"],"len":len(chat_info)}}
        return jsonify(result)

@chat.route("/update/chat/<int:chatid>", methods=['POST'])
def update(chatid):
    print(chatid)
    print(chat_list[chatid])
    lengs=len(chat_list[chatid])-1
    result={"len":lengs}
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
        c.close()
        return render_template("chat2.html", chat_list=chat_info, link_chatid=chatid, tpl_room_name=room_name, tpl_my_id=my_id)
    else:
        return redirect("/login2")


# チャット送信時のプログラム
@chat.route("/chat/<int:chatid>", methods=["POST"])
def chat_post(chatid):
    if "user_id" in session:
        # ここにチャットの送信ボタンが押されたときにDBに格納するプログラム
        my_id = session["user_id"]
        current_time = datetime.datetime.now()
        time= current_time.strftime("%m/%d,%I:%M %p")

        chat_message = request.form.get("input_message")
        
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
                  (chatid, to_id, my_id, chat_message,time,"text"))
        conn.commit()
        c.close()
        chat_list[chatid].append(chat_message)
        return redirect("/chat/{}".format(chatid))
    else:
        return redirect("/login2")


# ログイン画面表示
@chat.route("/login2")
def login_get():
    return render_template("login2.html")


# ログインするプログラム。
@chat.route("/login2", methods=["POST"])
def login():
    name = request.form.get("username")
    password = request.form.get("password")
    
    if name==""or password=="":
        return render_template("login2.html")
    password = cash(password)
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    c.execute(
        "select id from user where name = ? and password = ?", (name, password))
    user_id = c.fetchone()
    conn.close()
    print(type(user_id))
    if user_id is None:
        return render_template("login2.html")
    else:
        session['user_id'] = user_id[0]
        return redirect("/userlist2")


# アカウント作成(新規ユーザー登録)プログラム
@chat.route("/regist", methods=["POST"])
def regist():
    name = request.form.get("username")
    password = request.form.get("password")
    if name==""or password=="":
        return render_template("login2.html")
    special_characters_pattern = r'[!@#$%^&*()_+{\[\]:;<>,.?~\\|/-]'
    if re.search(special_characters_pattern, name) or re.search(special_characters_pattern, password):
        return render_template("login2.html")
    password = cash(password)
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    # 同じ名前のユーザーが既に存在するか確認
    c.execute("SELECT id FROM user WHERE name = ?", (name,))
    existing_user = c.fetchone()

    # 既存のユーザーが存在する場合
    if existing_user:
        print("同じ名前のユーザーが既に存在します。登録できません。")
    else:
        c.execute("insert into user values(null,?,?)", (name, password))
        conn.commit()
    conn.close()
    return redirect("/login2")


# ログアウト
@chat.route("/logout2")
def logout():
    session.pop('user_id', None)
    return redirect("/login2")

import uuid

@chat.route('/chat/<int:chatid>/imgupload', methods=["POST"])
def imgupload(chatid):
    # URLでhttp://127.0.0.1:5000/uploadを指定したときはGETリクエストとなるのでこっち
    imagelist=['png', 'jpg',"jpeg", 'gif']
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    allowed_extensions = set(['png', 'jpg', 'gif','mp4'])  # 許可する拡張子のリスト
    file = request.files['example']

    if file:
        file_extension = file.filename.split('.')[-1]
        if file_extension in allowed_extensions:
            if file_extension  in imagelist:
                datatype="img"
            elif "mp4" == file_extension:
                datatype="video"
            
            hashfilename=str(hashlib.sha256(str(file.filename).encode("utf-8")).hexdigest())
            filename= hashfilename+str(uuid.uuid4())+file.filename
            while os.path.isfile("./static/images/chat/"+filename):
                filename= hashfilename+str(uuid.uuid4())+file.filename
            file.save(os.path.join('./static/images/chat', filename))
            chat_message="../static/images/chat/"+filename
            current_time = datetime.datetime.now()
            time= current_time.strftime("%m/%d,%I:%M %p")

            my_id = session["user_id"]
            conn = sqlite3.connect(chat_data_base)
            c = conn.cursor()
            c.execute(
                    "select user_id1, user_id2 from chat where id = ?", (chatid,))
            chat_user = c.fetchone()
            if my_id != chat_user[0]:
                to_id = chat_user[0]
            else:
                to_id = chat_user[1]
                
            c.execute("insert into chatmess values(null,?,?,?,?,?,?)",
                        (chatid, to_id, my_id, chat_message,time,datatype))
            conn.commit()
            chat_list[chatid].append(chat_message)
            return redirect("/chat/{}".format(chatid))
            
        else:
            return redirect("/chat/{}".format(chatid))
    else:
        return redirect("/chat/{}".format(chatid))
    
    