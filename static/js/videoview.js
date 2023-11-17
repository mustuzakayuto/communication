var socket = io(`https://witty-presently-hermit.ngrok-free.app/`);
const id = document.getElementById("id")
var viewurl = "videoid"+id.innerText
const image_id = document.getElementById("image")
var imagedata=image_id.src
const passbotn = document.getElementById("setpass")
const passwordelement = document.getElementById("password")

if(location.search!=""){

    
    viewurl+="pass"+location.search.split("?pass=")[1]
    
}
console.log(viewurl)
socket.emit('viewstart', {"id":id.innerText});


window.addEventListener('unload', function () {
    socket.emit('viewend', {"id":id.innerText});
});
function setpassfunction(){
    
    console.log()
    var url="?pass="+passwordelement.value
    window.location.href=url
    
    // viewurl = "stopvideo"+id.innerText+passwordelement.value
    
    
}
passbotn.addEventListener("click",setpassfunction)
var num=0
socket.on(viewurl, function(img){
    num++
    console.log(num)
    image_id.src = img;
});
var stopurl = "stopvideo"+id.innerText

socket.on(stopurl, function(data){
    
    image_id.src = imagedata;
});


const viewelment = document.getElementById("viewnum")
var viewnum=0
socket.on("viewstart"+id.innerText, function(data){
    viewnum++
    viewelment.innerText=viewnum
});
socket.on("viewend"+id.innerText, function(data){
    viewnum--
    viewelment.innerText=viewnum
});