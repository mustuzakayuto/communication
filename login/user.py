from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import database
import hashlib

bp = Blueprint('user', __name__)

@bp.route('/signup')
def sign_up():
    
    return render_template('signup.html')
# 追記
@bp.route('/login')
def log_in():
    return render_template('login.html')

@bp.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # SHA-256でハッシュ化
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
        return f"こんにちは。{session['username']}さん"
    else:
        flash('メンバーページにアクセスするにはログインしてください')
        return redirect(url_for('user.log_in'))

@bp.route('/logout')
def log_out():
    session.clear()
    return redirect(url_for('index'))








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
