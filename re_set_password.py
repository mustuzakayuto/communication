import flask 

import flask_wtf
import wtforms
from wtforms import validators
from itsdangerous.url_safe import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
import mail

import config
import sqlite3
import re
import hashlib
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
        print(new_password)
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
    ''' user_idからtokenを生成
    '''
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(user_id, salt=salt)
def load_token(token, secret_key, salt, max_age=600):
    ''' tokenからメールアドレスを取得
    '''
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.loads(token, salt=salt, max_age=max_age)
@reset_pass.route('/mail', methods=['GET', 'POST'])
def resetpass():
    ''' メールアドレスを入力してもらって
        パスワード変更画面のURLを通知する
    '''
    form = AddressForm()

    # ポストの場合のメール送信とメッセージ表示
    if flask.request.method == 'POST' and form.validate_on_submit():
        # TODO DBを参照して存在するメールアドレスか確認（割愛）
        if (is_email_exists(flask.request.form['mail'])):
            
            # 先ほど書いたcreate_tokenメソッドでtokenを生成
            token = create_token(form.mail.data, flask.current_app.config['SECRET_KEY'], SALT)
            # url = flask.url_for('new_pwd', token=token, _external=True)
            url = flask.url_for('reset_pass.new_pwd', token=token, _external=True)

            mail.main(flask.request.form['mail'],"パスワード変更",url)
            # メール送信を割愛してURLをページ表示
            flask.flash('メール送ったよ :')

    # ページ表示
    return flask.render_template(
            'mail.html',
            form=form)

@reset_pass.route('/new_pwd', methods=['GET', 'POST'])
def new_pwd():
    ''' 新規パスワード設定
    '''
    if flask.request.method == 'GET':

        # アドレスの取得
        try:
            token = flask.request.args.get('token')
            mail_address = load_token(token, flask.current_app.config['SECRET_KEY'], SALT)
        except Exception as e:
            return flask.abort(400)

        # ページ表示
        form = NewPwdForm(token=token)
        return flask.render_template(
                'new_pwd.html',
                form=form,
                mail_address=mail_address)
    else:
        form = NewPwdForm() 
        # アドレスの取得
        try:
            mail_address = load_token(form.token.data, flask.current_app.config['SECRET_KEY'], SALT)
        except Exception as e:
            return flask.abort(400)

        if form.validate_on_submit():
            # TODO ここにパスワードのudpate処理
            message= change_password(mail_address,flask.request.form['new_pwd2'])
            
            flask.flash(message)
            if message=="パスワードを更新しました":
                print("user.login")
                return flask.redirect(flask.url_for('user.log_in'))

        return flask.render_template(
                'new_pwd.html',
                form=form,
                mail_address=mail_address)

class AddressForm(flask_wtf.FlaskForm):
    mail = wtforms.StringField('mail', [
        validators.Email(message='メールアドレスの形式が間違っています'),
        validators.InputRequired(message='メールアドレスを入力してください')])
class NewPwdForm(flask_wtf.FlaskForm):
    token = wtforms.HiddenField('token', [
        validators.InputRequired()] )
    new_pwd1 = wtforms.PasswordField('パスワード', [
        validators.InputRequired(),
        validators.EqualTo('new_pwd2')] )
    new_pwd2 = wtforms.PasswordField('パスワード(確認用)', [
        validators.InputRequired()] )
