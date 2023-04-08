## Personnel Planet Capstone
#### Distinctiveness and Complexity
This project is a personnel management application where users sign up under a certain level of authority. This will allow the application to decide what the user can do or see which is unique in comparison to other projects from this course. Its use case is also unique compared to other projects because it has no intention of letting general users post which was a part of the both the marketplace and social media project.
This project also implements a unique level of complexety making use of Django Channels and JS websocket which was not utalized in the other projects in this course. This project uses a lot of bootstrap features to offer general styles to the diffrent sections of the application. 
Overall this project uses some new features of django and javascript not fully explored in this course to add some complexity and its functionality differs significantly from other projects use cases added to its distinctiveness.

#### Files and their purpose
##### HTML Files
In my templates folder there is a single subfolder named employer to contain the shift html used for employers due to the amount of diffrences between the employee and employer versions of this specific page. The employer shift page allows the user to see some basic employee information and create shifts for a selected employee using a dropdown menu.
The rest of the htmls are as listed home, login, logout, messages, profile, register, shift. 
In order their functionality is discribed as follows:
Home: This page has a memo slider showing information about the company, a static elearn div displaying courses the user could take or has completed (this is not dynamic per employee). It also has a clock in/out section to track an employees work. The only difference between employee and employer views is the ability for employers to post to the memo board.
Login, Register: Simple forms that allow users to login in or register an account linking them to a specific company. When a user registers they are asked for a first and last name that is then used to create a work id using their initals and some randomly generated numbers. Login then uses said work id. Logout of clears the users sessoin and redirects them to the login page.
Messages: This page uses Django Channels and JS websockets to connect a logged in user to a group of users that share the same company. These groups are then used to create a live chat environment for company members to communicate in a group chat session.
Profile: Acts as the users profile page allowing the user to change availability some personal information and also view tasks assigned by managemnet and also lists other employees names and roles at the company. The only difference between employee and employers are the ability to add to the task list. 
Shift: Allows the user to see some basic employee information and create shifts for a selected employee using a dropdown menu.
##### CSS FILES
This applications styles.css file contains all unique CSS for this course. The file is split up based on the view that it will be styling and the viewport that it will be supporting. It offers styles for the entire application.
The media section is responsible for the images used on the main home page for the E-learn section.

##### scripts.js 
This files main purpose is to communicate to the server depending on what the user is trying to do, while some aspects of the application do use direct post/get requests the JS file does include many asynchronous operations. This also holds the construction of the websocket connection for the messages page allowing live communication between the server and client. There are also many small changes to styles as well as some sections that change the html itself. This file also makes use of regular expressions to run certain sections of the JS depending on the url (the page the user is on). There are quite a few event listeners mostly focused on click events that make use of recursion to make fetch calls to the server. Using the fetch statements this file also loosly handles errors made during runtime.

##### VIEWS (and other added python folders)
The base django views file contains the views for all html pages and some basic get information for each view aside from the profile and authorization views that contain some post functionality.
Aside from the view functions there is also quite a few API functions that allow for users to asyncronusly get and post data to the django models for this project. These functions include but aren't limited to Clock in/out, get and update schedule and availability, get and update memo information, and other basic get, post and put funcationality utalized in this project.

An added consumers.py file holds functions for the django channels and live chat functionality these functions connect users to company groups then handles sending and recieving messages.

The routing.py file contains the websocket url used to tell django to look to the consumers file for channels functions.

Dockerignore, commands.txt, and Dockerfile folders are used to create a docker image and container for this project. 

Requirments.txt holds all the dependencies for this project

Procfile contains a commant important for the hosting service Heroku that this project is hosted on.



#### How to use
A user will first be prompted to login or create an account for the company that they are apart of. The user will then be redirected to the home page.
All pages of this project can be navigated to using the a navbar present on all pages. The home page contains a memo board tailored to the company 
the user is connected to. Below the user will have a clock in/out button that allows them to log hours, here they also find information about their daily and weekly hours along with a schedule for the day. On this page there is also a static eLearn page. Next the user can visit the shifts page as and employee they will see their hours for the current week and a dropdown that will let them choose to see the next weeks as well. An employer will see a diffrent page allowing them to select from employees and modify the shifts for each day. They will also see the employees availability. Next on our navbar is the message board here the employees and managment can communicate in a live chat using django channels each company has its own group chat. Finally is the profile page where the user can change personal information, availability and see task assigned to their team. They can also offer help or mark tasks as complete. There is also a list of all current employees of that company. An employer will be able to assign and remove tasks, change sensitve imformation about employees and terminate employees of their company. 
