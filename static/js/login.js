var username = document.getElementById("username")
var password = document.getElementById("password")


function rood(){
    fetch('/getuser', 
        {
            method: 'POST',
            
            body: JSON.stringify({"None":"None"}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if(result.username!="None"){
                username.value=result.username

            }            

        })

    .catch(error => {
        console.error('データの取得に失敗しました:', error);
    });
}