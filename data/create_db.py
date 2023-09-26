import sqlite3
import config
import os
def main():
    if os.path.isfile(config.DATABASE):
        os.remove(config.DATABASE)
    con = sqlite3.connect(config.DATABASE)
    con.execute("DROP TABLE IF EXISTS USERS")
    con.execute("CREATE TABLE USERS (\
        USERNAME TEXT PRIMARY KEY UNIQUE NOT NULL, \
        PASSWORD TEXT NOT NULL, \
        USEREMAIL TEXT NOT NULL)"  # USEREMAIL カラムを追加
    )
    print('データベースを初期化しました')



if __name__ == '__main__':
    main()