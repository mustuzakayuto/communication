var username
var menu = document.getElementById("menu")
function getusername(){
    
    fetch('/sessionusername', {
        method: 'POST',
        body: JSON.stringify({ "None":"None" }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
       
        console.log(result.sessionusername);
        username = result.sessionusername
        console.log("username:"+username,username,username=="None")
        // usernameがセッションに存在するかチェック
        if (username!= "None") {
        // セッションにusernameが存在する場合の処理
        menu.innerHTML+='<p><a href="/face_emotion" class="left box1">表情感情分析</a></p>'
        menu.innerHTML+='<p><a href="/create_image_index" class="left box1">画像生成</a></p>'
        //   console.log('セッションにusernameが存在します:', username);
        } else {
        // セッションにusernameが存在しない場合の処理
        console.log('セッションにusernameは存在しません');
        }
        
    })
    .catch(error => {
        console.error(error);
    });
    console.log(sessionStorage.getItem("username"))
    console.log(username)
    
    

}
// セッションストレージからusernameを取得
getusername()
