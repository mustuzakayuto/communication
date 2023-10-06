import os
def setup(port):
    # 現在のユーザー名を取得
    current_user = os.getlogin()

    # ngrok.ymlファイルのパスを構築
    ngrok_yml_path = os.path.join("C:\\Users", current_user, ".ngrok2", "ngrok.yml")

    # ngrok_yml_pathを使ってファイルにアクセスするコードを記述
    # 例えば、ngrok_yml_pathを使ってファイルを読み込む場合は以下のようになります
    with open(ngrok_yml_path, "r") as ngrok_yml_file:
        ngrok_yml_contents = ngrok_yml_file.readlines()

    # ngrok_yml_contentsにファイルの内容が格納されます
    print(ngrok_yml_contents)


    with open(ngrok_yml_path, "w") as ngrok_yml_file:
        domain=input("domain name:")
        for txt in ngrok_yml_contents:
            if "addr" in txt:
                txt = "    addr: "+str(port)+"\n"
            elif "hostname" in txt:
                txt="    hostname: "+domain+"\n"
            ngrok_yml_file.write(txt)
        
def portset(port):
        # 現在のユーザー名を取得
    current_user = os.getlogin()

    # ngrok.ymlファイルのパスを構築
    ngrok_yml_path = os.path.join("C:\\Users", current_user, ".ngrok2", "ngrok.yml")

    # ngrok_yml_pathを使ってファイルにアクセスするコードを記述
    # 例えば、ngrok_yml_pathを使ってファイルを読み込む場合は以下のようになります
    with open(ngrok_yml_path, "r") as ngrok_yml_file:
        ngrok_yml_contents = ngrok_yml_file.readlines()

    # ngrok_yml_contentsにファイルの内容が格納されます
    


    with open(ngrok_yml_path, "w") as ngrok_yml_file:
        
        for txt in ngrok_yml_contents:
            if "addr" in txt:
                txt = "    addr: "+str(port)+"\n"

            ngrok_yml_file.write(txt)
