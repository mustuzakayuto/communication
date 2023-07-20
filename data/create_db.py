import sqlite3
import os

def main():
    path = os.getcwd()
    os.chdir(path+'/data')
    con = sqlite3.connect('users.db')
    con.execute("DROP TABLE IF EXISTS USERS")
    con.execute("CREATE TABLE USERS (\
        USERNAME TEXT PRIMARY KEY UNIQUE NOT NULL, \
        PASSWORD TEXT NOT NULL)"
    )
    print('データベースを初期化しました')


if __name__ == '__main__':
    main()