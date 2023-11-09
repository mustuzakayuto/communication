const Result = document.getElementById("result")
Vue.createApp({
    data() {
        return {
            video: null,
            canvas: null,
            context: null,
            display_result:null,
            copybutton:null,
            dataUrl: '',
            status: 'none'
        }
    },
    methods: {
        // ① カメラとキャンバスの準備
        initialize() {

            this.status = 'initialize';

            navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: {
                        ideal: 'environment'
                    }
                }
            })
            .then(stream => {

                this.canvas = this.$refs.canvas;
                this.display_result = document.getElementById("result")
                this.copybutton = document.getElementById("copy")

                this.copybutton.addEventListener('click', () => {
                if (!navigator.clipboard) {
                    alert("このブラウザは対応していません");
                    return;
                }
                
                
                navigator.clipboard.writeText(this.display_result.innerText).then(
                    () => {
                        
                    alert('文章をコピーしました。');
                    },
                    () => {
                    alert('コピーに失敗しました。');
                    });
                });

                this.context = this.canvas.getContext('2d');

                this.video = document.createElement('video');
                this.video.addEventListener('loadedmetadata', () => { // メタデータが取得できるようになったら実行

                    const canvasContainer = this.$refs['canvas-container'];
                    this.canvas.width = canvasContainer.offsetWidth;
                    this.canvas.height = parseInt(this.canvas.width * this.video.videoHeight / this.video.videoWidth);
                    this.render();

                });
                // iOSのために以下３つの設定が必要
                this.video.setAttribute('autoplay', '');
                this.video.setAttribute('muted', '');
                this.video.setAttribute('playsinline', '');
                this.video.srcObject = stream;
                this.playVideo();

            })
            .catch(error => console.log(error));

        },
        render() {

            if(this.video.readyState === this.video.HAVE_ENOUGH_DATA) {

                this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);

            }

            requestAnimationFrame(this.render);

        },
        
        runOcr() { // ③ スナップショットからテキストを抽出

            this.status = 'reading';
            
            
            fetch('/ocr', {
                method: 'POST',
                body: JSON.stringify({"image_data": this.dataUrl }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(result => {
                console.log("結果:"+result.data.text)
                
                this.display_result.innerText=result.data.text
                this.status="play"
                
                
            })
            .catch(error => {
                console.error(error);
            }).finally(() => {

                this.playVideo();

            });
            

            

        },
        playVideo() {

            this.video.play();
            this.status = 'play';

        },
        pauseVideo() {

            this.video.pause();
            this.status = 'pause';

        },
        takeSnapshot() { // ② スナップショットを取る（カメラは一時停止）

            // this.makeSound(); // 音を鳴らす
            this.pauseVideo();
            console.log(this.canvas.toDataURL())
            this.dataUrl = this.canvas.toDataURL();

        },
        makeSound() { // ④ おまけ：スナップショットをとるときに音をならす

            document.querySelectorAll('.notification-iframe').forEach(el => el.remove()); // 全ての通知用 iFrame を削除

            // soundタグは使わず iFrame で直接音声ファイルへアクセスする
            const iFrame = document.createElement('iframe');
            iFrame.setAttribute('src', '/audios/insight.ogg');
            iFrame.setAttribute('allow', 'autoplay');
            iFrame.style.display = 'none';
            iFrame.className = 'notification-iframe';
            document.body.appendChild(iFrame);

        }
    },
    mounted() {

        this.initialize();

    }
}).mount('#app');


function translation(text){
    fetch('/translation', 
        {
            method: 'POST',
            
            body: JSON.stringify({"txt":text}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)
            text = result.text
            console.log(result.text)
            
            
        })
}

// const copybutton = document.getElementById("copy")

// copybutton.addEventListener('click', () => {
//   if (!navigator.clipboard) {
//     alert("このブラウザは対応していません");
//     return;
//   }
//   console.log("log"+Result.innerText)
  
//   navigator.clipboard.writeText(Result.innerText).then(
//     () => {
        
//       alert('文章をコピーしました。');
//     },
//     () => {
//       alert('コピーに失敗しました。');
//     });
// });

