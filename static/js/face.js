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

function endEmotionDetection() {
    activeVideo = false;
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
}

async function startEmotionDetection() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        activeVideo = true;
        frameTime = 0;

        function captureFrame() {
            if (frameTime % frameRate === 0) {
                console.log(frameTime)
                const context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
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
                    if (result.len !== 0) {
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