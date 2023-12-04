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
    domain=input("domain name:")
    istunnels=False
    for data in ngrok_yml_contents:
        if "tunnels" in data:
            istunnels=True

    with open(ngrok_yml_path, "w") as ngrok_yml_file:
        
        for txt in ngrok_yml_contents:
            
            ngrok_yml_file.write(txt)
        if not istunnels:
            ngrok_yml_file.write("tunnels:\n")
        ngrok_yml_file.write("  ITalk:\n")
        ngrok_yml_file.write("    addr: "+str(port)+"\n")
        ngrok_yml_file.write("    proto: http\n")
        ngrok_yml_file.write("    hostname: "+domain+"\n")
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
        
        for index in range(len(ngrok_yml_contents)):
            print(index,type(index))            

            
            if "ITalk" in ngrok_yml_contents[index]:
                print(ngrok_yml_contents[index+1])
                ngrok_yml_contents[index+1]=f"    addr: {port} \n"
                
            ngrok_yml_file.write(ngrok_yml_contents[index])