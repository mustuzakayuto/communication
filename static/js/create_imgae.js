const createimage = document.getElementById('PROMPT');
const Result3 = document.getElementById("imgcreateresult")
const showMODEL = document.getElementById('show_MODEL_ID');
var MODEL_ID = "normal"
console.log(MODEL_ID)
setMODEL()
function nomal(){
    MODEL_ID= "normal"
    console.log(MODEL_ID)
    setMODEL()
}
function anima(){
    MODEL_ID ="Anime_style"
    console.log(MODEL_ID)
    setMODEL()
}
function real(){
    MODEL_ID ="real"
    console.log(MODEL_ID)
    setMODEL()
}
function setMODEL(){
    showMODEL.innerHTML = MODEL_ID
}
function startcreateimagefunction(){
    Result3.innerHTML="<h3>順番に生成しているのでお待ちください</h3>"
    // const searchdata = {"search":search.value}
    fetch('/image', {
        method: 'POST',
        
        body: JSON.stringify({"array":{"PROMPT":createimage.value,"MODEL_ID":MODEL_ID}}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        console.log(result);

        Result3.innerHTML = '<img src='+result.img+' alt="" class="create_image">'
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}

const startcreate = document.getElementById('startcreate');
startcreate.addEventListener('click', startcreateimagefunction);

const txtdata = document.getElementById('inputdata');
const Result = document.getElementById("translationresult")
function starttranslationfunction(){
    // const searchdata = {"search":search.value}
    fetch('/translation', {
        method: 'POST',
        
        body: JSON.stringify({"txt":txtdata.value}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
    .then(result => {
        console.log(result);

        Result.textContent = result.txt
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}

const starttranslation = document.getElementById('starttranslation');
starttranslation.addEventListener('click', starttranslationfunction);


const copybutton = getElementById("copy")

copybutton.addEventListener('click', () => {
  if (!navigator.clipboard) {
    alert("このブラウザは対応していません");
    return;
  }

  navigator.clipboard.writeText(Result.textContent).then(
    () => {
      alert('文章をコピーしました。');
    },
    () => {
      alert('コピーに失敗しました。');
    });
});