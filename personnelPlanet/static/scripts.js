let availObj = {
    monday: '',
    tuesday: '',
    wednesday: '',
    thursday: '',
    friday: '',
    saturday: '',
    sunday: ''
}
const userId = JSON.parse(document.getElementById('id').textContent);
const firstName = JSON.parse(document.getElementById('firstName').textContent);
const date = new Date()
// APIS
function clockIn(){
    // SEND POST REQUEST AND HANDLE REST IN VIEW
    fetch('/clock', {
        method: 'POST',
    }).then(response => response)
    .then(result => alert(result))
    .catch(err => alert(err))
}
function clockOut(){
    // SENT PUT REQUEST AND HANDLE REST IN VIEW
    fetch('/clock', {
        method: 'PUT',
    }).then(response => response)
    .then(result => alert(result))
    .catch(err => alert(err))
}

function send_message(body){
    
    fetch('/messages', {
        method: 'POST',
        body: JSON.stringify({
            body: body
        })
    }).then(response => response)
        .then(result => console.log(result))
        .catch(err => console.log(err))
    
}
function updateMemo(memoId, memoUpdate){
    // memo update should be an object in memo model format and memo id is for edits if memo id = 0 then we are creating a new memo
    if (!memoUpdate && memoId !== 'memoNotice'){
        fetch('/memo',{
            method: 'PUT',
            body: JSON.stringify({
                memoId: memoId
            })
        }).then(response => response)
        .then(result => alert(result))
        .catch(err => alert(err))
    }
    else if (memoId === 'new'){
        console.log(memoUpdate)
        fetch('/memo',{
            method: 'POST',
            body: JSON.stringify({
                subject: memoUpdate['subject'],
                body: memoUpdate['body']
            })
        }).then(response => response)
        .then(result => alert(result))
        .catch(err => alert(err))
        
    }
}
function sendSchedule(schedule, workerId){
    fetch('/shifts', {
        method: 'POST',
        body: JSON.stringify({
            schedule: schedule,
            workerId: workerId,
        })
        })
    .then(response => response.json)
    .then(result=> console.log(result))
    .catch(err => console.log(err))
}
function availability(userAvailability) {
    
    fetch(`/availability`, {
        method: 'POST',
        body: JSON.stringify({
            body: userAvailability,
        })
    }).then(response => response.json)
    .then(result=> console.log(result))
    .catch(err => console.log(err))
}
function schedules(workerId){
    fetch(`/schedules/${workerId}`, {
        method: 'GET',
    }).then(response => response.json())
    .then(result => {
        let schedule = result.schedule
        let scheduleArr = []
        for(let day in schedule){
            if (typeof schedule[day] === 'string'){    
                scheduleArr.push(schedule[day].split('-'))
            }
            console.log(schedule[day])
        }
        console.log(scheduleArr)
        let daysInput = document.querySelectorAll('.scheduling-input')
        console.log(daysInput)
        for(let i = 0; i < 7; i++){
            daysInput[i].value = scheduleArr[i][0] 
            daysInput[i + 7].value = scheduleArr[i][1] 
        }


    })
    .catch(err => console.log(err))
}

document.addEventListener("DOMContentLoaded", () => {
    regUserCircle = document.querySelector("#reg-user-circle");
    if (window.innerWidth < 650){
        regUserCircle.setAttribute("color", "#63ACE5");
        console.log(regUserCircle)
    }
    //-------------------- PROFILE AVAIL TABLE SCRIPTS --------------------------//
    if (/\bprofile\b/gi.test(window.location.href)){
        console.log('working');
        let allCells = document.querySelectorAll('.avail-cell')
        allCells.forEach(cell => {
            // --------------  CHANGES BG ON HOVER  ------------------ //
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
            // -------------  CHANGES BG AND POPULATES availObj  ------------------- //
            cell.addEventListener('click', () => {
                let test = cell.attributes.id.value;
                let split = test.split('-');
                let day = split[1];

                allCells.forEach(item =>{  
                    if (item.attributes.id.value.includes(`${day}`) && item != cell){
                        
                        item.style.backgroundColor = '';
                    }
                })
                
                if (cell.style.backgroundColor !== 'limegreen'){
                    cell.style.backgroundColor = 'limegreen';
                    availObj[split[1]] = split[0];
                }else{
                    cell.style.backgroundColor = '';

                }
                console.log(availObj)
            });
        })
        // -----------------  RESETS AVAIL TABLE  ------------------------- //
        document.querySelector("#reset-avail").addEventListener('click', () => {
            allCells.forEach(cell => {
                cell.style.backgroundColor = ''
            })
            for (var day in availObj) availObj[day] = '';
            console.log(availObj)
        })
        document.querySelector("#submit-avail").addEventListener('click', (e) => {
        e.preventDefault()
        availability(availObj);
        console.log(availObj);
    })
    }
    // SHIFT MAKER FUNCTION
    else if (/\bshifts\b/gi.test(window.location.href)){
        let scheduleDropdown = document.querySelector("#employee-schedule-dropdown")
        let submitSchedule = document.querySelector("#submit-schedule")
        let resetChanges= document.querySelector("#reset-changes")
        let saveChanges = document.querySelector("#shift-save")
        let workerId = scheduleDropdown.value
        scheduleDropdown.addEventListener('change', () =>{
            workerId = scheduleDropdown.value
            schedules(workerId)
        })

        submitSchedule.addEventListener('click', () =>{
            let daysInput = document.querySelectorAll('.scheduling-input')
            let regex = /\d{1,2}:\d{2}/;
            // Use regex to test all values for format when looping first 7 are start times last are end times
            
            let isCleanData = true;
            daysInput.forEach(day => {
                if(day.value != 'off' && !regex.test(day.value)){
                    isCleanData = false;
                }
            })
            if (!isCleanData){alert('Make sure all times are in the proper format hh:mm');}
            else{$('#shift-change-modal').modal('show')}
            let sortedDaysArr = []
            saveChanges.addEventListener('click', () =>{
                for (let i = 0; i < 7; i++){
                    sortedDaysArr.push(`${daysInput[i].value}-${daysInput[i + 7].value}`)
                }
                console.log(sortedDaysArr, workerId, 'here')
                sendSchedule(sortedDaysArr, workerId)
                
                sortedDaysArr = [];
        });
        })

    }
    else if (/\bmessages\b/gi.test(window.location.href)){
        let url = `ws://${window.location.host}/ws/socket-server/`
        const messageSocket = new WebSocket(url)
        allMsgCont = document.querySelector('#all-messages-container')
        allMsgCont.scrollTo(0, 100000)
        messageSocket.onmessage = function(e){
            let data = JSON.parse(e.data)
            console.log(data)
            if(data.type === "message"){
                sec = document.createElement('section')
                if (data.userId === userId){
                sec.classList.add('single-message-container', 'fromUser')
                }else{
                    sec.classList.add('single-message-container')  
                }
                
                head = document.createElement('h6')
                head.classList.add('single-message-username')
                body = document.createElement('p')
                body.classList.add('single-message-body')
                ts = document.createElement('p')
                ts.classList.add('single-message-timestamp')
                head.innerText = data.name;
                body.innerText = data.message;
                let day = date.getDate();
                let month = date.getMonth();
                ts.innerText = `${month}/${day}`;
                sec.appendChild(head)
                sec.appendChild(body)
                sec.appendChild(ts)
                msgCont = document.querySelector('#all-messages-container')
                msgCont.insertBefore(sec, msgCont.lastElementChild)
                allMsgCont.scrollTo(0, 100000)
            }
        }
        document.querySelector('#button-addon2').addEventListener('click', () =>{
            
            msgBody = document.querySelector('#msg-body').value;
            send_message(msgBody)
            document.querySelector('#msg-body').value = '';
            messageSocket.send(JSON.stringify({
                'message': msgBody,
                'userId': userId,
                'name': firstName
            }))


            
           
        });
    }
    else if (/\b\b/gi.test(window.location.href)){
        let memoId = 0;
        document.querySelector('#remove-memo').addEventListener('click', () =>{
            let memoList = document.querySelectorAll('.carousel-item')
            let memoSubject = ''
            memoList.forEach(memo => {
                if (memo.classList.contains('active')){
                    memoId = memo.id
                    console.log(memo);
                    memoSubject = memo.childNodes[1].childNodes[1].innerText;

                }
            })
            document.querySelector('#remove-memo-check').innerText = `Remove memo ${memoSubject}`
            document.querySelector('#remove-memo-confirm').addEventListener('click', () =>{
                updateMemo(memoId, false);
            })
                
            console.log(memoSubject);
        });
        document.querySelector('#submit-memo').addEventListener('click', () =>{
            let memoObj = {
                subject: document.querySelector('#memo-subject-input').value,
                body: document.querySelector('#memo-body-input').value
            }
            updateMemo('new', memoObj);
        })
        document.querySelector('#clock-in').addEventListener('click', () =>{
            clockIn();
        });
        document.querySelector('#clock-out').addEventListener('click', () =>{
            clockOut();
        });
    }

})