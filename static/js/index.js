function getPassword (){
   
    var chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + 
    'abcdefghijklmnopqrstuvwxyz0123456789@#$';;

    var passwordLenght = 12;
    var passwordgen = ""
    for (var i=0; i<passwordLenght; i++){
        console.log(i)
        var randomNumber = Math.floor(Math.random()* chars.length)
        passwordgen +=chars.substring(randomNumber, randomNumber +1);


    }
    console.log(passwordgen)
    document.getElementById("pass").value = passwordgen
}

function showpass(){
    document.getElementById("pass").setAttribute("type", "text")
    
    var data = document.getElementById("hidepass").innerHTML;
    console.log(data)
    if (data == "hide password"){
        document.getElementById("pass").setAttribute("type", "password")
    }
    document.getElementById("hidepass").innerHTML="hide password"


}
