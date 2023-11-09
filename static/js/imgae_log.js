
const Result3 = document.getElementById("imgcreateresult")

function startcreateimagefunction(){
    
    // const searchdata = {"search":search.value}
    fetch('/imagelog', {
        method: 'POST',
        
        body: JSON.stringify({"None":"None"}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        console.log(result);
        
        
        for(var int=result.arr.img_list.length-1;int>=0;int--) {
            var div = document.createElement("div")
            var img =  document.createElement("img")
            var time =  document.createElement("p")
            var prompt = document.createElement("p")
            
            var dl_button = document.createElement("button")

            dl_button.addEventListener('click', dl_img);
            dl_button.value=result.arr.img_list[int]
            dl_button.innerText="ダウンロード"
            div.className="chip"
            div.id=int
            img.className="create_image"
            time.className="resulttxt time"
            prompt.className="resulttxt back-white"
            
            img.src=result.arr.img_list[int]
            
            time.innerHTML=result.arr.times[int]
            prompt.innerHTML=result.arr.prompt[int]

            div.appendChild(img)
            div.appendChild(time)
            div.appendChild(prompt)
            div.appendChild(dl_button)


            Result3.appendChild(div)
            
            // Result3.innerHTML += '<img src='+imgpath+' alt="" class="create_image">'
        };
       
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}
function dl_img(event){
    
    var imagename=event.target.value
    var imagenamelist=imagename.split("/")
    console.log(imagename)
    imagename=imagenamelist[imagenamelist.length-1]
    console.log(imagename)
    fetch('/download_img', {
        method: 'POST',
        
        body: JSON.stringify({"imgname":imagename}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((response) => {
        // レスポンスからファイルデータを取得
        return response.blob();
      })
      .then((blob) => {
        // ブラウザでファイルを保存するためのリンクを作成
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
  
        // ファイル名を指定（必要に応じて変更）
        a.download = imagename;
  
        // リンクをクリックしてダウンロードを開始
        a.click();
  
        // メモリリークを防ぐために URL オブジェクトを解放
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error('ファイルのダウンロード中にエラーが発生しました:', error);
      });
}

startcreateimagefunction()