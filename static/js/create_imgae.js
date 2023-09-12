const createimage = document.getElementById('PROMPT');
const Result3 = document.getElementById("imgcreateresult")

function startcreateimagefunction(){
    // const searchdata = {"search":search.value}
    fetch('/image', {
        method: 'POST',
        
        body: JSON.stringify({"PROMPT":createimage.value}),
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

        Result.innerHTML = "<h2>"+result.txt+'</h2>'
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}

const starttranslation = document.getElementById('starttranslation');
starttranslation.addEventListener('click', starttranslationfunction);