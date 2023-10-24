var lengs=0
function update(){
    
    fetch('/update', 
        {
            method: 'POST',
            
            body: JSON.stringify({"None":"None"}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
        .then(result => {
            if(lengs!=result.lengs){
                display_switching()
            }
        })

    .catch(error => {
        console.error('データの取得に失敗しました:', error);
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
    sleep(5, function() {
    
        update()
        loop()
    });
}
loop()