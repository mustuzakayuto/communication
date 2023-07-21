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