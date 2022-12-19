

document.addEventListener("DOMContentLoaded", () => {
    regUserCircle = document.querySelector("#reg-user-circle");
    if (window.innerWidth < 650){
        regUserCircle.setAttribute("color", "#63ACE5");
        console.log(regUserCircle)
    }
    //-------------------- PROFILE AVAIL TABLE SCRIPTS --------------------------//
    if (/\bprofile\b/gi.test(window.location.href)){
        console.log('working');
    }
    document.querySelectorAll('.avail-cell').forEach(cell => {
        console.log(cell)
        cell.addEventListener('mouseover', () => {
            if (cell.style.backgroundColor !== 'limegreen'){
                cell.style.backgroundColor = 'lightgreen';
            }
        })
        cell.addEventListener('mouseout', () => {
            if (cell.style.backgroundColor != 'limegreen'){
                cell.style.backgroundColor = '';
            }
        });
        cell.addEventListener('click', () => {
            if (cell.style.backgroundColor !== 'limegreen'){
                cell.style.backgroundColor = 'limegreen';
            }else{
                cell.style.backgroundColor = '';
            }
        });
    })


})