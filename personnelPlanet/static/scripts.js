document.addEventListener("DOMContentLoaded", () => {
    regUserCircle = document.querySelector("#reg-user-circle");
    
    if (window.innerWidth < 650){
        regUserCircle.setAttribute("color", "lightgrey");
        console.log(regUserCircle)
    }

})