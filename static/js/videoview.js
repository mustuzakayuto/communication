const Result = document.getElementById("result")
function view(){
    fetch(location.pathname, {
        method: 'POST',
        body: JSON.stringify({ "None":"None"}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        Result.innerHTML=""
        console.log(result);
        var img = document.createElement("img")
        img.src=result.data
        Result.appendChild(img)
        
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
        view()
        loop();
    });
}
loop()