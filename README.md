## Personnel Planet Capstone
#### Distinctiveness and Complexity
This project is a mock personnel management application designed to support a company in handling basic employee information and communication.
It differs from the other projects in this course in its functionality and goals, this project implements a closed group communication not meant for general use like the social network. 

#### Files and their purpose
##### HTML Files
In my templates folder there is a single subfolder named employer to contain the shift html used for employers due to the amount of diffrences between the employee and employer versions of this specific page. The employer shift page allows the user to see some basic employee information and create shifts for a selected employee using a dropdown menu.
The rest of the htmls are as listed home, login, logout, messages, profile, register, shift. 
In order their functionality is discribed as follows:
Home: This page has a memo slider showing information about the company, a static elearn div displaying courses the user could take or has completed (this is not dynamic per employee). It also has a clock in/out section to track an employees work. The only difference between employee and employer views is the ability for employers to post to the memo board.
Login, Register: Simple forms that allow users to login in or register an account linking them to a specific company. When a user registers they are asked for a first and last name that is then used to create a work id using their initals and some randomly generated numbers. Login then uses said work id. Logout of clears the users sessoin and redirects them to the login page.
Messages: This page uses Django Channels and JS websockets to connect a logged in user to a group of users that share the same company. These groups are then used to create a live chat environment for company members to communicate in a group chat session.
Profile: Acts as the users profile page allowing the user to change availability some personal information and also view tasks assigned by managemnet and also lists other employees names and roles at the company. The only difference between employee and employers are the ability to add to the task list. 
Shift: This page operates as explained above.
##### CSS FILES
Regretably there is only one CSS file for this prohect in the static folder. This combersome file includes all styles for desktop and mobile versions of all the html files for this project in scale these file should have been split up at very least by the viewport size.
##### VIEWS (and other added python folders)
The base django views file contains the views for all html pages and some basic get information for each view aside from the profile and authorization views that contain some post functionality.
Aside from the view functions there is also quite a few API functions that allow for users to asyncronusly get and post data to the django models for this project. These functions include but aren't limited to Clock in/out, get and update schedule and availability, get and update memo information, and other basic get, post and put funcationality utalized in this project.

An added consumers.py file holds functions for the django channels and live chat functionality these functions connect users to company groups then handles sending and recieving messages.

The routing.py file contains the websocket url used to tell django to look to the consumers file for channels functions.

Dockerignore, commands.txt, and Dockerfile folders are used to create a docker image and container for this project. 

Requirments.txt holds all the dependencies for this project

#### How to use
When a user accesses this project they have the option to join a company as an Employer or an Employee if the company does not exist one is created.
Company and user information is stored in a realational database. Once a company is created and a user is signed in the main display across the app for employee and employers are quite similar with the only real diffrennce in the employers ability to add and remove from certain sections of the app. The home page has a memo board where employers can give important updates, a clock in/out button and a discription of your shift and if you are on the clock, a display of current time spent on the clock and hours worked for the week. A static eLearn section is also displayed as a way to fill some of the whitespace on desktops. Employees see an option for a shift page that when clicked will redirect the user to a page that simply displays their schedule for the week. An employers shift page is labled employees and allows the employer to select employees from a drop down and schedule that employee as well as display said employees availability. A messages page is the next nav link and it connects the user to a django channel websocket group linked by the users company name. This page is a live chat page for that company that displays a users name a message and a date that the message was sent. The final page is the profile page which again only differs in that the employer can create tasks and assign employees to tasks. Once a task is assigned and created users can either mark as complete or offer help if that task isnt completed. Once the task is marked the employer can close that task out. There is also a list of employees and their role in the company. A section with personal information that the user can change. Only select information can be changed. And finally their is an availabitlity table that simply allows users to click cells of a table to chose a between morning evening or open availability. In scale there are many things I could add or change about this project but I do believe that in its current state this project has tought me quite a bit and is sufficient for the scope of this final project. 