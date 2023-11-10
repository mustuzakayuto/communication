
const videoElem = document.getElementById("video");
const startElem = document.getElementById("start");
const stopElem = document.getElementById("stop");
const canvasElem = document.getElementById("canvas")
var is_video = false;
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
}
function uprode(){
    canvasElem.width = videoElem.videoWidth;
    canvasElem.height = videoElem.videoHeight;
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/png');
    fetch(location.pathname, {
        method: 'POST',
        body: JSON.stringify({ "frame":frame }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        
    })
    .catch(error => {
        console.error(error);
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
    sleep(3, function() {
        if (is_video){
            uprode();
        }
        loop();
    });
}
loop()