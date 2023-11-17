const id = document.getElementById("id")
const videoElem = document.getElementById("video");
const startElem = document.getElementById("start");
const stopElem = document.getElementById("stop");
const canvasElem = document.getElementById("canvas")

var password="null";
var is_video = false;
var socket = io(`https://witty-presently-hermit.ngrok-free.app/`);

// Options for getDisplayMedia()
var displayMediaOptions = {
    video: {
        cursor: "always"
    },
    audio: false
};

// Set event listeners for the start and stop buttons
startElem.addEventListener("click", function (evt) {
    startCapture();
    is_video=true;
}, false);

stopElem.addEventListener("click", function (evt) {
    stopCapture();
    is_video=false;
}, false);

async function startCapture() {
    try {
        videoElem.srcObject = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
    } catch (err) {
        console.error("Error: " + err);
    }
}

function stopCapture(evt) {
    let tracks = videoElem.srcObject.getTracks();

    tracks.forEach(track => track.stop());
    videoElem.srcObject = null;
    socket.emit('stopvideo', {"id":id.innerText});
}

function uprode(){
    canvasElem.width = videoElem.videoWidth;
    canvasElem.height = videoElem.videoHeight;
    var context = canvas.getContext('2d');
    context.drawImage(videoElem, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/png');
    socket.emit('video', {frame,"id":id.innerText,password});
}
const passbotn = document.getElementById("setpass")
const passwordelement = document.getElementById("password")
function setpassfunction(){
    password=passwordelement.value
    passwordelement.value=""
    
}
passbotn.addEventListener("click",setpassfunction)
const viewelment = document.getElementById("viewnum")
var viewnum=0
viewelment.innerText=viewnum

socket.on("viewstart"+id.innerText, function(data){
    viewnum++
    viewelment.innerText=viewnum
});
socket.on("viewend"+id.innerText, function(data){
    viewnum--
    viewelment.innerText=viewnum
});
const FPS = 60;



setInterval(() => {
    if (is_video)uprode()
    
}, 10000/FPS)
