const input = document.getElementById('input');
const reply = document.getElementById('result');
const transmission = document.getElementById('transmission');
var inputdata
function chat_transmission(){
    inputdata = input.value
    fetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ inputdata }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        reply.innerText = result.result
    })
}


transmission.addEventListener('click', chat_transmission);


const speech = new webkitSpeechRecognition();
speech.lang = 'ja-JP';

const btn = document.getElementById('btn');
const content = document.getElementById('content');

btn.addEventListener('click' , function() {
    speech.start();
});

speech.onresult = function(e) {
        speech.stop();
        if(e.results[0].isFinal){
            var autotext =  e.results[0][0].transcript
            content.innerHTML += '<div>'+ autotext +'</div>';
        }
    }

    speech.onend = () => { 
    speech.start() 
    };