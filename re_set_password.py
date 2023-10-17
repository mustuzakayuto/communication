import flask 

from wtforms import Form, PasswordField, HiddenField,validators
from itsdangerous.url_safe import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
import re
import hashlib
import sqlite3

import mail
import config




reset_pass = flask.Blueprint("reset_pass",__name__)

SALT = 'shio'

def is_email_exists(email):
    con = sqlite3.connect(config.DATABASE)
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS WHERE USEREMAIL = ?", (email,))
    result = cur.fetchone()
    con.close()
    return result is not None

def change_password(email, new_password):
    if is_email_exists(email):
        # 特殊文字を含む正規表現パターン
        special_characters_pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\|/-]'
        if re.search(special_characters_pattern, new_password):
            return "特殊文字を含まないでください"
        hashed_password = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        
        con = sqlite3.connect(config.DATABASE)
        cur = con.cursor()
        cur.execute("UPDATE USERS SET PASSWORD = ? WHERE USEREMAIL = ?", (generate_password_hash(hashed_password), email))
        con.commit()
        con.close()
        return "パスワードを更新しました"
    return "メールアドレスが設定されていません"

def create_token(user_id, secret_key, salt):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(user_id, salt=salt)

def load_token(token, secret_key, salt, max_age=600):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.loads(token, salt=salt, max_age=max_age)

@reset_pass.route('/mail', methods=['GET', 'POST'])
def resetpass():
    if flask.request.method == 'POST':
        email = flask.request.form.get('mail')
        if email:
            if is_email_exists(email):
                token = create_token(email, flask.current_app.config['SECRET_KEY'], SALT)
                url = flask.url_for('reset_pass.new_pwd', token=token, _external=True)
                mail.main(email, "パスワード変更", url)
                flask.flash('メール送ったよ :)')
            else:
                flask.flash('メールアドレスが存在しません')
    return flask.render_template('mail.html')

@reset_pass.route('/new_pwd', methods=['GET', 'POST'])
def new_pwd():
    if flask.request.method == 'GET':
        token = flask.request.args.get('token')
        if token:
            try:
                mail_address = load_token(token, flask.current_app.config['SECRET_KEY'], SALT)
                form = NewPwdForm()
                return flask.render_template('new_pwd.html', form=form, mail_address=mail_address)
            except Exception as e:
                return flask.abort(400)
    elif flask.request.method == 'POST':
        token = flask.request.form.get('token')
        new_password = flask.request.form.get('new_pwd2')
        if token and new_password:
            try:
                mail_address = load_token(token, flask.current_app.config['SECRET_KEY'], SALT)
                message = change_password(mail_address, new_password)
                flask.flash(message)
                if message == "パスワードを更新しました":
                    return flask.redirect(flask.url_for('user.log_in'))
            except Exception as e:
                return flask.abort(400)
    return flask.render_template('new_pwd.html', form=NewPwdForm(), mail_address='')




class NewPwdForm(Form):
    token = HiddenField('token')
    new_pwd1 = PasswordField('新しいパスワード', [
        validators.InputRequired(message='パスワードを入力してください'),
        validators.EqualTo('new_pwd2', message='パスワードが一致しません')
    ])
    new_pwd2 = PasswordField('新しいパスワード（確認用）', [
        validators.InputRequired(message='パスワードを再入力してください')
    ])
