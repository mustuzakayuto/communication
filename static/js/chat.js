const chatMessage = document.getElementById("chatMessage");

var country = "None" 
const country_name = document.getElementsByName("country-name");
// プルダウンメニュー要素を取得
const countrySelector = document.getElementById('country-selector');

const Language_box = document.getElementById("Language-box")
var is_road = false
var len=0
// 選択肢が変更されたときに呼び出される関数
function updateSelectedLanguage() {
    const selectedOption = countrySelector.options[countrySelector.selectedIndex];
    const selectedValue = selectedOption.value;
    // const selectedText = selectedOption.textContent;
    country=selectedValue
    set_session()
    console.log(country)
    
    
}


// 選択肢が変更されたときに関数を呼び出すリスナーを追加
countrySelector.addEventListener('change', updateSelectedLanguage);

function select(){
    

    // 選択を変更
    for (let i = 0; i < countrySelector.options.length; i++) {
        if (countrySelector.options[i].value === country) {
            countrySelector.selectedIndex = i;
            console.log(countrySelector.options[i].value)
            break;
        }
    }

    
}

console.log(country)   

function set_session(){
    fetch('/session', 
        {
            method: 'POST',
            
            body: JSON.stringify({"country":country}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        
    .catch(error => {
        console.error('データの取得に失敗しました:', error);
    });
}


function display_switching(){
    
    var json = {"is_road":is_road.toString()}
    console.log(json)
    chatMessage.innerHTML=""
    chatMessage.innerText=""
    // サーバーからchat_listを非同期で取得
    fetch('/get_chat_list'+location.pathname, 
        {
            method: 'POST',
            
            body: JSON.stringify(json),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        .then(response => response.json())
        .then(result => {
            // 取得したデータを処理し、DOMに表示する
            displayChatList(result.data.chat_list,result.data.my_id);
            country=result.data.type
            console.log(result.data.chat_list,result.data.type)
            select()
            len=result.data.len
            is_road=true
            // ページロード時に初期値を設定
            updateSelectedLanguage();
            
        })
    .catch(error => {
        console.error('データの取得に失敗しました:', error);
    });

    
}

// chat_listを表示する関数
function displayChatList(chatList,tpl_my_id) {
    
    var i=0
    // chatListをループしてDOMに追加
    chatList.forEach(chat => {
        var chatElement = document.createElement('p');
        var time = document.createElement("time")
        
        
        if ( chat.type=="text"){
            var translation = document.createElement("button")
            translation.addEventListener('click', translationtxt);
            translation.innerText="翻訳"
            translation.value=chat.message
            translation.className="translation"
            
            var maindata = document.createElement("span");
            maindata.innerText=`${chat.fromname}: ${chat.message}`;
            maindata.id=i
            maindata.className=chat.type
            
        }else if(chat.type=="img"){
            var imgdata = document.createElement("img");
            var maindata = document.createElement("span");
            maindata.innerHTML = chat.fromname+"  :"
            console.log(chat.message)
            imgdata.src=chat.message
            imgdata.id=i
            imgdata.className="show-img"
            
            maindata.className=chat.type
            maindata.appendChild(imgdata)
        }else if(chat.type=="video"){
            
            var maindata = document.createElement("span");
            var video = document.createElement("video")
            maindata.innerHTML = chat.fromname+"  :"
            video.width=
            video.src=chat.message
            video.id=i
            video.className="show-video"
            
            video.controls = true;  // 'controls'属性を追加
            video.muted = true;     // 'muted'属性を追加
            video.autoplay = true;  // 'autoplay'属性を追加
            video.playsInline = true;  // 'playsinline'属性を追加
            video.loop = true;      // 'loop'属性を追加
            maindata.className=chat.type
            maindata.appendChild(video)


        }
        
        
        time.innerText="  "+chat.time+"  "
        time.className="time"
        if (chat.from==tpl_my_id){
            chatElement.className="fromText"
            
        }else{
            chatElement.className="toText"
        }
        
        
        
        
        if (chat.from==tpl_my_id){
            
            
            chatElement.appendChild(time);
            chatElement.appendChild(maindata);
            
            if(chat.type=="text")chatElement.appendChild(translation)
            
        }else{
            if(chat.type=="text")chatElement.appendChild(translation)
            chatElement.appendChild(maindata);
            chatElement.appendChild(time);
            
            
        }
        
        chatMessage.appendChild(chatElement)

        i++
    });
    }
function scrollToBottom() {
    var elementHeight = chatMessage.clientHeight;

    // 要素のスクロール可能な高さ
    var elementScrollHeight = chatMessage.scrollHeight;

    // 要素内の一番下の位置
    var bottomPosition = elementScrollHeight - elementHeight;

    chatMessage.scrollTop=bottomPosition
}
function scrollToTop() {
    chatMessage.scrollTop=0
}
function translationtxt(event){
    
    var target = event.target.parentElement
    console.log(target)
    var innerText = target.querySelector('span').innerText
    var username = innerText.split(":")[0]
    var txt = innerText.split(":")[1]
    var id = target.querySelector('span').getAttribute('id')
    console.log(id)
    console.log(location.pathname)
    fetch('/translation'+location.pathname, 
        {
            method: 'POST',
            
            body: JSON.stringify({"data":{"txt":txt,"id":id}}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)
            txt = result.txt
            console.log(result.txt)
            console.log(txt)
            console.log("txt")
            console.log(txt)
            var span = document.getElementById(id)
            var message = username+":"+txt
            console.log(message)
            span.innerHTML=message
        })
    
}

function update(){
    
    fetch('/update'+location.pathname, 
        {
            method: 'POST',
            
            body: JSON.stringify({"None":"None"}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)
            
            if(len!=result.len){
                console.log(result.chats,len)
                is_road = false
                display_switching()
            }
        })

    .catch(error => {
        console.error('データの取得に失敗しました:', error);
    });
}

function sleep(waitSec, callbackFunc) {

    var spanedSec = 0;
  
    var waitFunc = function () {
  
        spanedSec++;
  
        if (spanedSec >= waitSec) {
            if (callbackFunc) callbackFunc();
            return;
        }
  
        clearTimeout(id);
        id = setTimeout(waitFunc, 1000);
    
    };
  
    var id = setTimeout(waitFunc, 1000);
  
}
function loop(){
    sleep(5, function() {
    
        update()
        loop()
    });
}

display_switching()
loop()
