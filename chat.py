from flask import *   # Flaskのなかみを全部持ってくる
import sqlite3  # sqliteつかいます
import config
import hashlib
chat=Blueprint("chat",__name__)
chat_data_base = config.CHATDATABASE

def cash(password):
    password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return password
@chat.route("/celchat")
def jump():
    return redirect("/login2")


# ユーザーを全て表示
@chat.route("/userlist2")
def userlist():
    conn = sqlite3.connect(chat_data_base)
    c = conn.cursor()
    c.execute("select id, name from user")
    user_info = c.fetchall()
    conn.close()
    return render_template("userlist2.html", tpl_user_info=user_info)


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
        if chat_id == None:

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
            "select id, room from chat where user_id1 = ? or user_id2 = ?", (my_id, my_id))
        chat_list = c.fetchall()
        return render_template("/chatroom2.html", tpl_chat_list=chat_list)
    else:
        return redirect("/login2")


# チャットルーム表示
@chat.route("/chat/<int:chatid>")
def chat_get(chatid):
    if "user_id" in session:
        my_id = session["user_id"]
        # ここにチャットをDBからとって、表示するプログラム
        conn = sqlite3.connect(chat_data_base)
        c = conn.cursor()
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
        c.execute("insert into chatmess values(null,?,?,?,?)",
                  (chatid, to_id, my_id, chat_message))
        conn.commit()
        c.close()

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

import re
# アカウント作成(新規ユーザー登録)プログラム
@chat.route("/regist", methods=["POST"])
def regist():
    name = request.form.get("username")
    password = request.form.get("password")
    if name==""or password=="":
        return render_template("login2.html")
    special_characters_pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\|/-]'
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



