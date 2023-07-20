from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import database
import hashlib
# インスタンス化
bp = Blueprint('user', __name__)

# (ipアドレス:5000)/signupと入力で表示
@bp.route('/signup')
def sign_up():
    
    return render_template('signup.html')

# (ipアドレス:5000)/loginと入力で表示
@bp.route('/login')
def log_in():
    return render_template('login.html')


@bp.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        # 名前とパスワード取得
        username = request.form['username']
        password = request.form['password']
        # SHA-256でハッシュ化 (暗号化)
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        db = database.get_db()

        user = db.execute(
            "SELECT * FROM USERS WHERE USERNAME = ?", (username, )
        ).fetchone()
        
        if user is None:
            flash('ユーザー名が間違っています')
        elif not check_password_hash(user['PASSWORD'], password):
            flash('パスワードが間違っています')
        else:
            session.pop('username', None)
            session['username'] = username
            return redirect(url_for('user.member'))
        return redirect(url_for('user.log_in'))

    return redirect(url_for('index'))

@bp.route('/member')
def member():
    if 'username' in session:
        return render_template('delete.html')
    else:
        flash('メンバーページにアクセスするにはログインしてください')
        return redirect(url_for('user.log_in'))

# (ipアドレス:5000)/log_outと入力で表示
@bp.route('/logout')
def log_out():
    session.clear()
    return redirect(url_for('index'))

# データベースから削除処理
@bp.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        # 名前とパスワード取得
        username = request.form['username']
        password = request.form['password']
        # SHA-256でハッシュ化 (暗号化)
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        db = database.get_db()

        user = db.execute(
            "SELECT * FROM USERS WHERE USERNAME = ?", (username, )
        ).fetchone()
        
        if user is None:
            flash('ユーザー名が間違っています')
        elif not check_password_hash(user['PASSWORD'], password):
            flash('パスワードが間違っています')
        else:
            if 'username' in session:
                username = session['username']
                db = database.get_db()
                db.execute("DELETE FROM USERS WHERE USERNAME = ?", (username,))
                db.commit()
                session.clear()
                flash(f'ユーザー「{username}」を削除しました')
    return redirect(url_for('index'))





# ユーザ登録
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # SHA-256でハッシュ化
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        db = database.get_db()
        user = db.execute(
            "SELECT * FROM USERS WHERE USERNAME = ?", (username, )
        ).fetchone()

        if user:
            flash(f'ユーザー「{username}」はすでに存在しています')
            return redirect(url_for('user.sign_up'))

        db.execute(
            "INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)",
            
            
            
            (username, generate_password_hash(password))
        )
        db.commit()
        return 'ユーザー登録が完了しました'

    return redirect(url_for('index'))
