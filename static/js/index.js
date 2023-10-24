const list = [
    "旅行先を選ぶとしたらどこに行きたいですか？",
    "好きな趣味や特技は何ですか？",
    "最後に読んだ本は何ですか？",
    "将来の夢や目標はありますか？",
    "好きな食べ物は何ですか？",
    "最近の楽しい出来事を教えてください。",
    "好きな映画やテレビ番組は何ですか？",
    "週末にする予定のことは何ですか？",
    "子どもの頃の思い出を教えてください。",
    "今欲しいものや購入したいものは何ですか？",
    "最近始めた新しいことはありますか？",
    "あなたの人生での最大の成就は何ですか？",
    "好きな季節や天気は何ですか？",
    "特別な日にしたいことや計画はありますか？",
    "過去に挑戦したことで一番難しかったことは何ですか？",
    "あなたのパーソナルトリビアを教えてください。",
    "好きな音楽やアーティストは何ですか？",
    "最後に笑ったことを教えてください。",
    "自分自身を三つの言葉で表現するとしたら何ですか？",
    "夢中になっていることは何ですか？",
    "好きな動物は何ですか？",
    "過去にした冒険や挑戦的なことを教えてください。",
    "あなたの人生でのモットーは何ですか？",
    "最後に感動したことを教えてください。",
    "他の国や文化に興味がありますか？",
    "人生での一番大きな後悔は何ですか？",
    "好きなスポーツやアクティビティは何ですか？",
    "他人から感銘を受けた人物はいますか？",
    "これからチャレンジしたいことや学びたいことは何ですか？",
    "最も大切にしている価値観は何ですか？",
    "好きな場所や空間はどこですか？",
    "人生での一番困難だった瞬間は何ですか？",
    "好きな色やデザインは何ですか？",
    "自分の強みや特長を教えてください。",
    "何か新しいことに挑戦する予定はありますか？",
    "好きな言葉や名言は何ですか？",
    "他人との関係性で大切にしていることは何ですか？",
    "最も楽しかった思い出を教えてください。",
    "好きな季節や行事は何ですか？",
    "人生での転機や変化を教えてください。",
    "あなたのストレスを解消する方法は何ですか？",
    "好きな飲み物や飲み物の組み合わせは何ですか？",
    "最後に驚いたことを教えてください。",
    "成功とは何だと思いますか？",
    "人生の中での目標や計画を教えてください。",
    "自分を振り返ってどんな成長を感じますか？",
    "何か他の人が驚くような特技や秘密の能力はありますか？",
    "周りの人によくされる質問は何ですか？",
    "過去の失敗から学んだことを教えてください。",
    "人生での最大の達成感を教えてください。",
    "好きな形やパターンは何ですか？",
    "大切にしている友情や人間関係を教えてください。",
    "自分の価値観や信念を三つ挙げてみてください。",
    "何か他人にアドバイスすることがあれば教えてください。",
    "好きなアウトドアアクティビティは何ですか？",
    "人生でのハードルや障害を乗り越えた経験を教えてください。",
    "あなたの秘密の楽しみや贅沢は何ですか？",
    "好きな料理や食べ物の組み合わせは何ですか？",
    "どんな人物になりたいと思っていますか？",
    "人生での成功の定義や意味を教えてください。",
]
const frame = {"ランキング":"ランキング"}

const content = document.getElementById('content');

function setValues(Values) {

    content.innerHTML = ""
    console.log(content.innerHTML)
    content.innerHTML += '<h3>'+ "注目のトピック" +'</h3>';
    content.innerHTML += '<button onclick="rerod()">リロード</button>'
    for (const value of Values) {
        content.innerHTML += '<div>'+ value +'</div>';
    }
    
}

function rerod(){
    fetch('/Ranking', {
        method: 'POST',
        
        body: JSON.stringify({ frame }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        
            setValues(result.arr);
        
    })
    .catch(error => {
        console.error(error);
    });
}

function randomselect(min,max){
    return Math.floor(Math.random() * (max - min)) + min;
}

const topic = document.getElementById('topic');
let topicvalue;
function startEmotionDetection(){
    topicvalue = list[randomselect(0,list.length)]
    console.log(topicvalue)
    topic.innerText = topicvalue
    
}

const startButton = document.getElementById('startButton');
startButton.addEventListener('click', startEmotionDetection);

const search = document.getElementById('search');
const Result = document.getElementById("result")
function startsearchfunction(){
    // const searchdata = {"search":search.value}
    fetch('/search', {
        method: 'POST',
        
        body: JSON.stringify({"search":search.value}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        Result.innerHTML="";
        for (const data of result.arr) {
            Result.innerHTML+=data+"<br>"
        }
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}

const startsearch = document.getElementById('startsearch');
startsearch.addEventListener('click', startsearchfunction);
const search_Results_Page = document.getElementById("search_Results_Page")
const pageresult = document.getElementById('pageresult');
function Results_Page(){
    fetch('/search_Results_Page', {
        method: 'POST',
        
        body: JSON.stringify({"search":search_Results_Page.value}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        pageresult.innerHTML="";
        console.log(result.title)
        console.log(result.title.length)
        for (var i=0 ;i<= result.title.length-1;i++) {
            

            if(result.title[i]!="Not Found" ){
                pageresult.innerHTML += "<h6>"+'<a href="'+result.link[i]+'">'+result.title[i]+'</a>'+"</h6>"
            }
        }
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}


const getsearch_Results_Page = document.getElementById("getsearch_Results_Page")
getsearch_Results_Page.addEventListener("click",Results_Page)
startEmotionDetection()
rerod()