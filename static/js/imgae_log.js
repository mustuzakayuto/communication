
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
        
        
        for(var int=0;int<result.arr.img_list.length;int++) {
            var div = document.createElement("div")
            var img =  document.createElement("img")
            var time =  document.createElement("p")
            var prompt = document.createElement("p")
            
            div.className="chip"
            img.className="create_image"
            time.className="resulttxt"
            prompt.className="resulttxt"
            
            img.src=result.arr.img_list[int]
            
            time.innerHTML=result.arr.times[int]
            prompt.innerHTML=result.arr.prompt[int]

            div.appendChild(img)
            div.appendChild(time)
            div.appendChild(prompt)


            Result3.appendChild(div)
            
            // Result3.innerHTML += '<img src='+imgpath+' alt="" class="create_image">'
        };
       
        // Result.value=result.arr;
        
    })
    .catch(error => {
        console.error(error);
    });
}

startcreateimagefunction()