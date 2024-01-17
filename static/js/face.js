const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startButton = document.getElementById('startButton');
const endButton = document.getElementById('endButton');
const angry = document.getElementById('angry');
const fear = document.getElementById('fear');
const happy = document.getElementById('happy');
const sad = document.getElementById('sad');
const surprise = document.getElementById('surprise');
const neutral = document.getElementById('neutral');

let stream;
let activeVideo = false;
let frameTime = 0;
const frameRate = 120;

function setEmotionValues(emotionValues) {
    angry.innerHTML = `怒り: ${(emotionValues.angry * 100).toFixed()}%`;
    fear.innerHTML = `恐怖: ${(emotionValues.fear * 100).toFixed()}%`;
    happy.innerHTML = `幸せ: ${(emotionValues.happy * 100).toFixed()}%`;
    sad.innerHTML = `悲しみ: ${(emotionValues.sad * 100).toFixed()}%`;
    surprise.innerHTML = `驚き: ${(emotionValues.surprise * 100).toFixed()}%`;
    neutral.innerHTML = `無感情: ${(emotionValues.neutral * 100).toFixed()}%`;
}
function facechange(facedata){
    if(facedata=="angry"){
        message="怒り"
   }else if(facedata=="disgust"){
        message ="嫌悪"
   }else if(facedata=="fear"){
        message="恐怖"
   }else if(facedata=="happy"){
        message="幸せ"
   }else if(facedata=="sad"){
        message="悲しみ"
   }else if(facedata=="surprise"){
        message="驚き"
   }else if(facedata=="neutral"){
        message="無感情"
   }
   return message


}
var average = document.getElementById("average")
function endEmotionDetection() {
    activeVideo = false;
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, 10000, 10000);
    stream.getTracks().forEach(track => {
        track.stop();
    });
    video.srcObject = null;
    setEmotionValues({
        angry: 0,
        disgust: 0,
        fear: 0,
        happy: 0,
        sad: 0,
        surprise: 0,
        neutral: 0,
    });
    fetch('/average', {
        method: 'POST',
        body: JSON.stringify({ "None":"None" }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        var message=""
        console.log(result)
       if(result.expression=="angry"){
            message="全体的に怒っている印象を受けます"
       }else if(result.expression=="disgust"){
            message ="全体的に嫌悪を感じている印象を受けます"
       }else if(result.expression=="fear"){
            message="全体的に恐怖を感じている印象を受けます"
       }else if(result.expression=="happy"){
            message="全体的に幸せを感じている印象を受けます"
       }else if(result.expression=="sad"){
            message="全体的に悲しんで印象を受けます"
       }else if(result.expression=="surprise"){
            message="全体的に驚いている印象を受けます"
       }else if(result.expression=="neutral"){
            message="全体的に無感情な印象を受けます"
       }
       if (message!=""){
            var messageelement=document.createElement("h3")
            var maxelement =document.createElement("h3")
            messageelement.innerText=message
            maxelement.innerText="最大の"+facechange(result.expression)+"は"+(result.maxface*100).toFixed()+"%"
            average.appendChild(messageelement)
            average.appendChild(maxelement)
            // average.innerHTML="<h3>"+message+"</h3>"
            // average.innerHTML+="<h3>"+"最大の"+facechange(result.expression)+"は"+(result.maxface*100).toFixed()+"%"+"</h3>"
       }
        // average.innerHTML = "average: "+"fear"+result.fear+"happy"+result.happy+"sad"+result.sad+"surprise"+result.surprise+"neutral"+result.neutral
        // average.innerHTML = "<h3>average:"+"怒り"+(result.angry*100).toFixed() +"%"+"嫌悪"+(result.disgust*100).toFixed() +"%"+"恐怖"+(result.fear*100).toFixed()+"%"+"幸せ"+(result.happy*100).toFixed()+"%"+"悲しみ"+(result.sad*100).toFixed()+"%"+"驚き"+(result.surprise*100).toFixed()+"%"+"無"+(result.neutral*100).toFixed()+"%"+"</h3>"
    })
    .catch(error => {
        console.error(error);
    });
}
function getvideosize(){
    canvas.width = video.videoWidth ;
    canvas.height = video.videoHeight ;
    
}

async function startEmotionDetection() {
    average.innerHTML = ""
    try {
        
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        activeVideo = true;
        frameTime = 0;
        canvas.width=180
        canvas.height=180
        
        function captureFrame() {
            if (frameTime % frameRate === 0) {
                getvideosize()
                console.log(frameTime)
                var context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                console.log(video.width,video.height,canvas.width,canvas.height)
                const frame = canvas.toDataURL('image/png');
                
                fetch('/upload', {
                    method: 'POST',
                    body: JSON.stringify({ frame }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    if (result.len != 0 & average.innerHTML=="") {
                        
                        setEmotionValues(result.arr);
                    }
                })
                .catch(error => {
                    console.error(error);
                });
            }
            frameTime += 1;

            if (activeVideo) {
                requestAnimationFrame(captureFrame);
            }
        }

        requestAnimationFrame(captureFrame);
    } catch (error) {
        console.error(error);
    }
}

startButton.addEventListener('click', startEmotionDetection);
endButton.addEventListener('click', endEmotionDetection);