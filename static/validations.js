function loginvalidation(){
    if (emailvalidation() && passvalidation()){
        document.getElementById("loginform").action= '/loginv/'
    }
    else{
        $("#loginform").one("click", function(event) {
            event.preventDefault();
          });
        swal({
            text: "Enter valid Credentials",
            icon: "warning"
            
          });
    }
}

function signupvalidation(){
    if (emailvalidation() && passvalidation() && phonevalidation()){
        document.getElementById("signupform").action= '/user/signupuser/'
    }
    else{
        $("#signupform").one("click", function(event) {
            event.preventDefault();
          });
        swal({
            text: "Enter valid Credentials",
            icon: "warning"
            
          });
    }
}

function phoneotpvalidation(){
    if (phonevalidation()){
        document.getElementById("loginotp").action= '/sendotp/'
    }
    else{
        $("#loginotp").one("click", function(event) {
            event.preventDefault();
          });
        swal({
            text: "Enter a valid Phone Number",
            icon: "warning",          
          });
    }
}

function updatevalidation(){
    if (emailvalidation() && namevalidation()){
        document.getElementById("updateform").action= '/admin/update/'
    }
}

function emailvalidation() {
    eregx = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
    email = document.getElementById("Email").value
    if (eregx.test(email)) {
        document.getElementById("evm").innerHTML = ''
        return true
    }
    else {
        document.getElementById("evm").innerHTML = 'Enter a valid Email'
        return false
    }
}

function passvalidation(){
    pregx = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,20}$/
    if(pregx.test(document.getElementById("Password").value))
    {
        document.getElementById("pvm").innerHTML = ''
        return true
    }
    else {
        document.getElementById("pvm").innerHTML = 'Enter a valid Password'
        return false
    }
}

function phonevalidation(){
    nregx = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im
    if(!nregx.test(document.getElementById("Phone").value))
    {
        document.getElementById("phvm").innerHTML = 'Enter a valid Phone Number'
        return false
    }
    else{
        document.getElementById("phvm").innerHTML = ''
        return true
    }
}


function namevalidation(){
    nregx = /^[A-Za-z]+$/
    if(!nregx.test(document.getElementById("Name").value))
    {
        document.getElementById("nvm").innerHTML = 'Enter a valid Name'
    }
    else{
        document.getElementById("nvm").innerHTML = ''
        return true
    }
}
