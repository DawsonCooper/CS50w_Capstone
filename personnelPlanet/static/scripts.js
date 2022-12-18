document.addEventListener("DOMContentLoaded", () => {
    regUserCircle = document.querySelector("#reg-user-circle");
    
    if (window.innerWidth < 650){
        regUserCircle.setAttribute("color", "#63ACE5");
        console.log(regUserCircle)
    }

})