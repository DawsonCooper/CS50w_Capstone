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
    let statusElem = document.getElementById('clockStat');
    // SEND POST REQUEST AND HANDLE REST IN VIEW
    fetch('/clock', {
        method: 'POST',
    }).then(response => response)
    .then(result => {
        statusElem.innerText = '';
        statusElem.innerText = 'Clock Status: On';
        alert('Clocked In')
    })
    .catch(err => alert(err))
}
function populate_tasks(taskList){
    // CREATE DOM ELEMENTS FOR EACH TASK AND APPEND TO #existing-tasks ELEMENT
    taskList.forEach(task => {
        taskWrapper = document.createElement('section');
        let complete = ''
        if (task.assignedTo.length > 10){
            task.assignedTo = task.assignedTo.replace(/[^a-zA-Z0-9]/g, ' ')
        }
        if (task.complete === true){
            complete = '<box-icon name="check" color="limegreen"></box-icon>'
        }
        let taskOfUser = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${task.assignedTo}${complete}</h5>
            <p class="card-text">${task.taskBody}</p>
            <a id='task-complete' onclick='task("","", true, "PUT", ${task.id})' value=${task.id} class='btn'>Mark Complete</a>
          </div>
        </div>`
        let taskOfCoworker = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">${task.assignedTo}${complete}</h5>
                <p class="card-text">${task.taskBody}</p>
                <a id='task-complete' value=${task.id} class='btn'>Offer Help</a>
            </div>
        </div>`
        let taskViewedByManager = `
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">${task.assignedTo}${complete}</h5>
            <p class="card-text">${task.taskBody}</p>
            <a id='task-complete' onclick='task("","", true, "PUT", ${task.id})' value=${task.id} class='btn'>Close task</a>
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
function task(assignTo='', taskBody='', status=false, method='', taskId = 0){
    
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
        console.log('in put')
        fetch('/task', {
            method: 'PUT',
            body: JSON.stringify({
                status: status,
                taskId: taskId
            })
        })
        .then(response => response.json())
        .then(result => console.log(result))
        .catch(error => alert(error));
    }
}
function clockOut(){
    // SENT PUT REQUEST AND HANDLE REST IN VIEW
    let statusElem = document.getElementById('clockStat');
    fetch('/clock', {
        method: 'PUT',
    }).then(response => response)
    .then(result => {
        statusElem.innerText = '';
        statusElem.innerText = 'Clock Status: Off';
        alert('Clocked Out')
    })
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
        .then(result => alert('Memo Modified'))
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
        .then(result => alert('Memo Added'))
        .catch(err => alert(err))
        
    }
}
function sendSchedule(schedule, workerId, week){
    fetch('/shifts', {
        method: 'POST',
        body: JSON.stringify({
            schedule: schedule,
            workerId: workerId,
            week: week,
        })
        })
    .then(response => response.json)
    .then(result=> alert('Shifts updated'))
    .catch(err => console.log(err))
}
function getScheduleByWeek(workerId, week){
    console.log({workerId})
    fetch(`/get_schedule_by_week/${workerId}/${week}`, {
        method: 'GET',
        })
    .then(response => response.json())
    .then(result=> genTables(result))
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
function genTables(result){
    console.log(result)
    let schedule = result.schedule
    console.log(schedule)
    delete schedule.week
    let scheduleArr = []
    for(let day in schedule){
        if (typeof schedule[day] === 'string'){    
            scheduleArr.push(schedule[day].split('-'))
        }
        console.log(schedule[day])
    }
    console.log({scheduleArr})
    
    let daysInput = document.querySelectorAll('.scheduling-input')
    let mobileDaysInput = document.querySelectorAll('.mobile-input')
    if (window.innerWidth > 800){
        if (isEmployer){
            for(let i = 0; i < 7; i++){
                daysInput[i].value = scheduleArr[i][0] 
                daysInput[i + 7].value = scheduleArr[i][1] 
            }
        }else{
            for(let i = 0; i < 7; i++){
                daysInput[i].innerText = scheduleArr[i][0] 
                daysInput[i + 7].innerText = scheduleArr[i][1]
            } 
        }
    }else{
        for(let i = 0; i < 14; i+=2){
            mobileDaysInput[i].value = scheduleArr[i/2][0] 
            mobileDaysInput[i + 1].value = scheduleArr[i/2][1] 
        }
    }

}
function schedules(workerId){
    fetch(`/schedules/${workerId}`, {
        method: 'GET',
    }).then(response => response.json())
    .then(result => {
        genTables(result)
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
    })
    .catch(error => console.log(error))

}
function empInfo(id, method='GET', workId='', payRate=0, company='', terminate = false){
    if (method == 'GET'){
        fetch(`empInfo/${id}`, {
            method: 'GET',
        }).then(response => response.json())
        .then(result => {
            let empObj = result.employee;
            console.log(empObj);
            document.getElementById('emp-workId').value = empObj['workId'];
            document.getElementById('emp-payRate').value = empObj['payRate'];
            document.getElementById('emp-company').value = empObj['company'];
        })
        .catch(error => alert(error))
    }
    else{
        fetch(`empInfo/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                workId: workId,
                payRate: payRate,
                company: company,
                terminate: terminate
            })
        }).then(response => response.json())
        .then(result => {
            if(confirm(result.message)){
                location.reload();
            }else{
                location.reload();
            }
            
        })
        .catch(error => alert(error))
    }
}
document.addEventListener("DOMContentLoaded", () => {
    if (/\bregister\b/gi.test(window.location.href)){
        document.querySelector('body').style.overflow = 'hidden'
    }
    //-------------------- PROFILE AVAIL TABLE SCRIPTS --------------------------//
    else if (/\bprofile\b/gi.test(window.location.href)){
        //STEP 1: FETCH FOR CURRENT USER AVAILABILITY
        
        get_availability(userId)
        task("","","","GET")
        //STEP 2: TARGET CELLS THAT ARE MARKED AS AVAILABLE AND TURN LIMEGREEN
        let empLinks = document.querySelectorAll('.emp-links')
        empLinks.forEach(link => {
            link.addEventListener('click', (e) =>{
                e.preventDefault();
                empId = link.id;
                empInfo(empId);
                let terminate = false;
                    document.querySelector('#emp-term').addEventListener('click', () =>{
                        if (terminate === true){
                            terminate = false;
                            document.querySelector('#term-message').innerText = 'You have deselected the termination process';
                        }else{
                        terminate = true;
                        document.querySelector('#term-message').innerText = 'You have selected to terminate this employee';
                        }
                    });
                document.getElementById('save-user-changes').addEventListener('click', () =>{
                    let workId = document.getElementById('emp-workId').value;
                    let payRate = document.getElementById('emp-payRate').value;
                    let company = document.getElementById('emp-company').value;
                    
                    empInfo(empId, 'PUT', workId, payRate, company, terminate);
                    
                })
            })
        })
        
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
                    
                });
            }
        })
        // -----------------  RESETS AVAIL TABLE  ------------------------- //
        document.querySelector("#reset-avail").addEventListener('click', () => {
            allCells.forEach(cell => {
                cell.style.backgroundColor = ''
            })
            for (var day in availObj) availObj[day] = '';
            
        })
        document.querySelector("#submit-avail").addEventListener('click', (e) => {
        e.preventDefault()
        availability(availObj);
        
    })
    // POST FETCH FOR TASK CREATION AND MODS //
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
        document.querySelector('#add-task-modal').style.display = 'none';
    });
    setTimeout(() => {
        let completeTask = document.querySelectorAll("#task-complete");
        console.log(completeTask)
        completeTask.forEach(task => {
            task.addEventListener('click', () => {
            console.log(task.innerText)
            if(task.innerText == 'Offer Help'){
                fetch('/addToTask', {
                    method: 'POST',
                    body: JSON.stringify({
                        taskId: task.value,
                    })  
                })
                .then((response) => response.json())
                .then((result) => {
                  alert("Success: You will be added to this task shortly!");
                })
                .catch((error) => {
                  console.error("Error:", error);
                });
            }
        });
        
    })
    }, 1000)
    
    

    // SELECT MENU CHECKBOX LSIT OF EMPLOYEES //
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
        // week range select menu
        let start = Date.now();
        console.log(start)
        let today = new Date();
        let day = today.getDay() || 7; 
        // checks if its monday and converts time
        if( day !== 1 )                
            today.setHours(-24 * (day - 1));  
        today = Date.parse(today);
        let days = 14;
        let dates = []

        for(let i=0; i<days; i++){
            dates.push(new Date(today + (i * 1000 * 60 * 60 * 24)).toDateString());
        }
        console.log(dates[0], dates[6])
        let option = document.createElement('option');
        
        let option2 = document.createElement('option');
        
        option.value = `${dates[0]} - ${dates[6]}`;
        option2.value = `${dates[7]} - ${dates[13]}`;
        option.innerText = `${dates[0]} - ${dates[6]}`;
        option2.innerText = `${dates[7]} - ${dates[13]}`;
        weekDropdown = document.getElementById('week')
        weekDropdown.appendChild(option)
        weekDropdown.appendChild(option2)
        
        // employer inputs
        if(isEmployer){
            let scheduleDropdown = document.querySelector("#employee-schedule-dropdown")
            let submitSchedule = document.querySelector("#submit-schedule")
            let resetChanges = document.querySelector("#reset-changes")
            let saveChanges = document.querySelector("#shift-save")
            let workerId = scheduleDropdown.value
            scheduleDropdown.addEventListener('change', () =>{
                document.querySelectorAll('.avail-cell').forEach(cell => {
                    cell.style.backgroundColor = '';
                })
                workerId = scheduleDropdown.value
                getScheduleByWeek(workerId, weekDropdown.value)
                get_availability(workerId)
            })
            resetChanges.addEventListener('click', () =>{
                document.querySelectorAll('.schedule-input').forEach(item =>{
                    
                    item.value = 'off'
                    item.placeholder = 'off'
                })
            });
            let regex = /\d{1,2}:\d{2}/;
            let isCleanData = true;
            weekDropdown.addEventListener('change',() =>{
                getScheduleByWeek(workerId, weekDropdown.value)
            })
            submitSchedule.addEventListener('click', () =>{
                if (window.innerWidth > 800){
                    let daysInput = document.querySelectorAll('.scheduling-input')
                    
                    // Use regex to test all values for format when looping first 7 are start times last are end times

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
                        if(week.value === 'Week' || workerId === 'Employees'){
                            alert('Please select a week and employee')
                        }else{
                            console.log('hello', week.value)
                            sendSchedule(sortedDaysArr, workerId, week.value)
                            sortedDaysArr = [];
                        }
                        
                    
                    });
                    
                }else{
                    let mobileDaysInput = document.querySelectorAll('.mobile-input')
                    // Use regex to test all values for format when looping first 7 are start times last are end times
                    mobileDaysInput.forEach(day => {
                        if(day.value != 'off' && !regex.test(day.value)){
                            isCleanData = false;
                        }
                    })
                    if (!isCleanData){alert('Make sure all times are in the proper format hh:mm');}
                    else{$('#shift-change-modal').modal('show')}
                    let mobileSortedArr = []
                    saveChanges.addEventListener('click', () =>{
                        for (let i = 0; i < 14; i+=2){
                            mobileSortedArr.push(`${mobileDaysInput[i].value}-${mobileDaysInput[i + 1].value}`)
                        }
                        
                        sendSchedule(mobileSortedArr, workerId)

                        mobileSortedArr = [];
                    
                    });
                    
                }
            })
        }else{
            weekDropdown.addEventListener('change',() =>{
                getScheduleByWeek(userId, weekDropdown.value)
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
    else if (/\blogin\b/gi.test(window.location.href)){
        document.querySelector('body').style.overflow = 'hidden'

        loginDumbBtn = document.querySelector('#login-dummy-button');
        loginDumbBtn.addEventListener('click',  () => {
            id= document.querySelector('#dummy-id').innerText;
            password= document.querySelector('#dummy-password').innerText;
            console.log({id, password});
            document.querySelector('#id_workId').value = id;
            document.querySelector('#id_password').value = password;
            document.querySelector('#login-submit').click();
        })
    }   

    else if (/\b\b/gi.test(window.location.href)){
        let memoId = 0;
        if (isEmployer){
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

            });
            document.querySelector('#submit-memo').addEventListener('click', () =>{
                let memoObj = {
                    subject: document.querySelector('#memo-subject-input').value,
                    body: document.querySelector('#memo-body-input').value
                }
                updateMemo('new', memoObj);
            })
        }   

        document.querySelector('#clock-in').addEventListener('click', () =>{
            clockIn();
        });
        document.querySelector('#clock-out').addEventListener('click', () =>{
            clockOut();
        });
        
    
    }
})