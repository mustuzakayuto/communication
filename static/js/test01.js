const nameElement = document.getElementById("name")
const mailElement = document.getElementById("mail")

fetch('/getaccount', {
    method: 'POST',
    
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(result => {
    nameElement.innerText = result.name
    mailElement.innerText = result.mail
})
.catch(error => {
    console.error(error);
});