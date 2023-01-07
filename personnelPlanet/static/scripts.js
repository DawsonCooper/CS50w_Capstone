let availObj = {
    monday: '',
    tuesday: '',
    wednesday: '',
    thursday: '',
    friday: '',
    saturday: '',
    sunday: ''
}

const firstName = JSON.parse(document.getElementById('firstName').textContent);
const userId = JSON.parse(document.getElementById('id').textContent);
const isEmployer = JSON.parse(document.getElementById('isEmployer').textContent);
const date = new Date()
const userWorkId = JSON.parse(document.getElementById('userWorkId').textContent);
// APIS
function clockIn(){
    // SEND POST REQUEST AND HANDLE REST IN VIEW
    fetch('/clock', {
        method: 'POST',
    }).then(response => response)
    .then(result => alert(result))
    .catch(err => alert(err))
}
function populate_tasks(taskList){
    console.log('made it')
    // CREATE DOM ELEMENTS FOR EACH TASK AND APPEND TO #existing-tasks ELEMENT
    taskList.forEach(task => {
        taskWrapper = document.createElement('section');
        let taskOfUser = `
        <div class="card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">${task.assignedTo}</h5>
            <p class="card-text">${task.taskBody}</p>
            <a href="#" id='task-complete' class='btn'>Mark Complete</a>
          </div>
        </div>`
        let taskOfCoworker = `
        <div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">${task.assignedTo}</h5>
                <p class="card-text">${task.taskBody}</p>
                <a href="#" id='task-complete' class='btn'>Offer Help</a>
            </div>
        </div>`
        let taskViewedByManager = `
        <div class="card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">${task.assignedTo}</h5>
            <p class="card-text">${task.taskBody}</p>
            <a href="#" id='task-complete' class='btn'>Close task</a>
          </div>
        </div>`
        if(isEmployer){
            taskWrapper.innerHTML += taskViewedByManager
        }
        else if(userWorkId == task.assignedTo) {
            taskWrapper.innerHTML += taskOfUser
        }else{
            taskWrapper.innerHTML += taskOfCoworker
        }

            
        document.querySelector('#existing-tasks').appendChild(taskWrapper)
    })

}
function task(assignTo='', taskBody='', status=false, method=''){
    
    if (method === 'POST'){
    // CREATE TASK
        fetch('/task', {
            method: 'POST',
            body: JSON.stringify({
                assignTo: assignTo,
                taskBody: taskBody,
                status: status,
            })
        })
        .then(response => response.json())
        .then(result => {method = 'GET';})
        .catch(err => alert(err));
    
    }
    else if (method === 'GET'){
    // GET TASKS
    console.log('called')
        fetch('/task', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(result => populate_tasks(result.taskList))
        .catch(error => console.log(error));
    }
    else{
    // update task status
    }
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
    }).then(response => response.json())
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
function get_availability(user){
    fetch(`/get_availability/${user}`, {
        method: 'GET',
    }).then(response => response.json())
    .then(result => {
        // Populates color on both mobile and desktop tables
        result['availability'].forEach(day => {
            let tableCellId = document.querySelectorAll(`#${day}`)
            tableCellId.forEach(cell => {
                cell.style.backgroundColor = 'limegreen';
            })
        })
        if(result['availability'] == false){
            console.log('caught in if')
            document.querySelectorAll('.avail-cell').forEach(cell => {
                    cell.style.backgroundColor = ''
                })
            }
        let allCells = document.querySelectorAll('.avail-cell')
        // SET INITAIL AVAIL OBJ 
        allCells.forEach(cell => {
            let test = cell.attributes.id.value;
            let split = test.split('-');  
            // CHECK TO SEE IF THE TABLE IS DISPLAYED (for submit on profile page)
            if (cell.offsetParent != null){
                if (cell.style.backgroundColor == 'limegreen'){
                    
                    availObj[split[1]] = split[0];
                }
        }
        
        })
        console.log(availObj)
    })
    .catch(error => console.log(error))

}

document.addEventListener("DOMContentLoaded", () => {
    if (/\bregister\b/gi.test(window.location.href || /\blogin\b/gi.test(window.location.href))){
        regUserCircle = document.querySelector("#reg-user-circle");
        if (window.innerWidth < 650){

            regUserCircle.setAttribute("color", "#63ACE5");
            console.log(regUserCircle)
        }
    }
    //-------------------- PROFILE AVAIL TABLE SCRIPTS --------------------------//
    else if (/\bprofile\b/gi.test(window.location.href)){
        //STEP 1: FETCH FOR CURRENT USER AVAILABILITY
        console.log(userId)
        get_availability(userId)
        task("","","","GET")
        //STEP 2: TARGET CELLS THAT ARE MARKED AS AVAILABLE AND TURN LIMEGREEN

        let allCells = document.querySelectorAll('.avail-cell')
        // SET INITAIL AVAIL OBJ 
        allCells.forEach(cell => {
            if (cell.offsetParent != null){
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
                        availObj[split[1]] = '';
                    }
                    console.log(availObj)
                });
            }
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
    // POST FETCH FOR TASK CREATION //
    let taskButton = document.querySelector("#submit-task");
    taskButton.addEventListener('click', () => {
        let taskBody = document.querySelector('#task-textarea').value;
        let empList = [];
        document.querySelectorAll('.employees-check').forEach(emp => {
            if (emp.checked){
                empList.push(emp.value);
            }
        })
        task(empList, taskBody, false, 'POST');
    });



    // SELECT MENU CHECKBOX LSIT OF EMPPLOYEES //
    let checkList = document.querySelector('#emp-list');
    checkList.getElementsByClassName('selector')[0].onclick = function(e) {
      if (checkList.classList.contains('visible'))
        checkList.classList.remove('visible');
      else
        checkList.classList.add('visible');
    }
    }
    // SHIFT MAKER FUNCTION
    else if (/\bshifts\b/gi.test(window.location.href)){
        if(isEmployer){
            let scheduleDropdown = document.querySelector("#employee-schedule-dropdown")
            let submitSchedule = document.querySelector("#submit-schedule")
            let resetChanges= document.querySelector("#reset-changes")
            let saveChanges = document.querySelector("#shift-save")
            let workerId = scheduleDropdown.value
            scheduleDropdown.addEventListener('change', () =>{
                workerId = scheduleDropdown.value
                schedules(workerId)
                get_availability(workerId)
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
                ts.innerText = `${month + 1}/${day}`;
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