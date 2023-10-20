def createdbpy():
    datalist=[]
    datalist.append("import sqlite3")
    datalist.append("import config")
    datalist.append("import os")
    datalist.append("def main():")
    

    
    filename=input("dbファイル名前")
    configname=input("config名前")
    table=input("table名前")

    datalist.append("    if os.path.isfile(config."+configname+"):")
    datalist.append("        os.remove(config."+configname+")")
    datalist.append("    # データベースに接続")
    datalist.append("    conn = sqlite3.connect(config.IMAGEDATABASE)")
    datalist.append("")
    datalist.append("    # カーソルを取得")
    datalist.append("    cursor = conn.cursor()")
    datalist.append("")
    datalist.append("    # テーブルを作成")
    datalist.append("    cursor.execute('''")
    datalist.append("        CREATE TABLE IF NOT EXISTS "+table+" (")
    
    while True:
        columnname=input("(カラム名前,end)")
        if columnname=="end":
            break
        columntype=input("カラムタイプ")
        datalist.append("            "+columnname+" "+columntype+",")
    datalist.append("            )")
    datalist.append("    ''')")
    datalist.append("")
    datalist.append("    # 変更をコミット")
    datalist.append("    conn.commit()")
    datalist.append("    # 接続を閉じる")
    datalist.append("    conn.close()")
    with open("data/create/"+filename+".py","w",encoding='utf-8') as f:
        for txt in datalist:
            f.write(txt+"\n")
    with open("config.py","a",encoding='utf-8') as f:
        f.write(configname+" = "+'"data/'+filename+'.db"\n')
    cdb=["from data.create import "+filename+"\n"]
    with open("create_data_base.py","r",encoding='utf-8') as f:
        cdb+=f.readlines()
    cdb.append(filename+".main()\n")
    with open("create_data_base.py","w",encoding='utf-8') as f:
        for txt in cdb:
            
            f.write(txt)
        
        
    
    with open("コントロール.py","r",encoding='utf-8') as f:
        cdb=f.readlines()
    dbname=input("input db name:")

    with open("コントロール.py","w",encoding='utf-8') as f:
        for txt in cdb:
            if "data_base=input" in txt:
                
                f.write(txt.split("):")[0]+dbname+'):")\n')
            elif "continue #表示" in txt:
                f.write("            get(config."+configname+',"'+table+'")\n')
                f.write(txt)
            elif "get(data_base,table)" in txt:
                f.write('        elif data_base=="'+table+'":\n')
                f.write("            data_base=config."+configname+"\n")
                f.write('            table="'+table+'"\n')
                f.write(txt)
            elif 'username = input("username:")' in txt:
                f.write('        elif data_base=="'+table+'":\n')
                f.write("            data_base=config."+configname+"\n")
                f.write(txt)
            else:

                f.write(txt)