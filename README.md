# Basic-Login-Signup-API
## #Requirement
Flask, 
flask-cors, 
flask-httpauth, 
flask-socketio, 
python-engineio, 
python-socketio 

## #What it does 
If multiple users are signed with same id and one of them changes the password, all others users will be logged out automatically ,except the one who has changed the password.

## How to use
Open app.py in your favourite Python IDE, install all the depedencies then run app.py(make sure all the .html, .db and .py are in same folder). Open Signup.html in any browser and signup with some username and password then it redirect you to index.html . Then if you want open another tab and login with same username & password and change the password from one of the tab. On a succesfull password change all other tab/tabs loged in with same userid will be logged out, except the one tab on which password has been changed. 
