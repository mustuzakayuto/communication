from data.get_data import get 
from data.rm_db import rm 

import config
import sqlite3

import subprocess
from createdb import createdbpy
tables={"emo":"emotions","user":"USERS","emave":"average","img":"images"}
def main():
    select = input('(db,start_server:start,createdbpy:cdbpy,flask):')
    if select=="start":
        # ターミナルで実行するコマンド
        command = "python app.py"
        # 新しいターミナルウィンドウを開いてコマンドを実行
        subprocess.Popen(["cmd.exe", "/c", "start", "cmd.exe", "/k", command])
    else:
        while True:
            
            if select=="db":
                select = input("(get,rm,wpy): ")
                if select=="get":
                    print("data base:")
                    data_base=input("(chat,emo,user,emave,img,all):")
                    
                    if data_base== "all":
                        get(config.CHATDATABASE,"user")
                        get(config.CHATDATABASE,"chat")
                        get(config.CHATDATABASE,"chatmess")  
                        get(config.EMOTIONDATABASE,"emotions")
                        get(config.DATABASE,"USERS")
                        get(config.EMOTIONAVERAGEDATABASE,"average")
                        get(config.IMAGEDATABASE,"images")
                        continue #表示
                    elif data_base=="chat":
                        data_base=config.CHATDATABASE
                        table=input("(user,chat,chatmess)")
                    elif data_base == "emo":
                        table=tables[data_base]
                        data_base=config.EMOTIONDATABASE
                    elif data_base=="user":
                        table=tables[data_base]
                        data_base=config.DATABASE
                    elif data_base=="emave":
                        table=tables[data_base]
                        data_base=config.EMOTIONAVERAGEDATABASE
                    elif data_base=="img":
                        table=tables[data_base]
                        data_base=config.IMAGEDATABASE
                    if input("(specific:sc):")=="specific":
                        column=input("カラム:")
                        intid=input("getdata")
                        get_data(data_base,table,column,intid)
                    else:       
                
                        get(data_base,table)
                elif select=="rm":
                    print("data base:")
                    data_base=input("(chat,emo,user,emave,img):")
                    if data_base=="chat":
                        data_base=config.CHATDATABASE
                        table=input("(user,chat,chatmess)")
                        if table=="chatmess":
                            select=input("all?[y:n]: ")
                            if select=="y":
                                start=input("start position:")
                                end=input("end position")
                                
                                for i in range(int(start),int(end)+1):
                                    idrm(data_base,table,str(i))
                                continue
                    elif data_base == "emo":
                        table=tables[data_base]
                        data_base=config.EMOTIONDATABASE
                    elif data_base=="user":
                        table=tables[data_base]
                        data_base=config.DATABASE
                    elif data_base=="emave":
                        table=tables[data_base]
                        data_base=config.EMOTIONAVERAGEDATABASE
                    elif data_base=="img":
                        table=tables[data_base]
                        data_base=config.IMAGEDATABASE
                        idint=input("id:")
                        idrm(data_base,table,idint)
                        get(data_base,table)
                        return

                    column= input("カラム")
                    username = input("消す値:")
                    rm(data_base,table,username,column)
                elif select=="wpy":
                    createdbpy()
            elif select=="flask":
                filename=input("file_name")
                app_name=input("app_name:")
                index_html=input("index_html")
                createflask(filename,app_name,index_html)
            elif select=="end":
                break
            select = input('(db,createdbpy:cdbpy,flask,end):')
def createflask(filename,app_name,index_html):
    with open("テンプレート.py","r",encoding='utf-8') as f:
        txts=f.readlines()
    with open(filename+".py","w",encoding='utf-8') as f:
        for txt in txts:
            txt=txt.replace('template', app_name)
            txt=txt.replace("index.html",'"'+index_html+'"')
            f.write(txt)
            
        
def idrm(data_base,table,id):
    # SQLite3データベースに接続
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()


    # ユーザー名が一致する行を削除するSQLクエリを実行
    cursor.execute(f"DELETE FROM {table} WHERE id=?", (id,))

    # 変更をコミット
    conn.commit()

    # データベース接続を閉じる
    conn.close()
def column(data_base,table,column,typedata):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute(f'ALTER TABLE {table} ADD {column} {typedata} FIRST;')

    # 変更をコミット
    conn.commit()

    # データベース接続を閉じる
    conn.close()
def get_data(data_base,table,column,intid):
    print()
    print("_____"+data_base,table+"________")
    # データベースに接続
    conn = sqlite3.connect(data_base)

    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリを実行
    cursor.execute(f"SELECT * FROM {table} WHERE {column}=?", (intid,))

    # 結果を取得
    data = cursor.fetchall()
    # print(data)
    # データを処理
    for row in data:
        print(row)

    # データベース接続を閉じる
    conn.close()
# column(config.IMAGEDATABASE,"images","time","TEXT")
main()
