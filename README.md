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

## #How to use
Open app.py in your favourite Python IDE, install all the dependencies then run app.py(make sure all the .html, .db and .py are in same folder). Open Signup.html in any browser and signup then it will redirect you to index.html . Then if you want open another tab and login with same username & password and change the password from one of the tab. On a successfully password change all other tab/tabs logged in with same user ID will be logged out, except the one tab on which password has been changed.

## Demo

https://user-images.githubusercontent.com/81517788/132939644-8e548b0e-38bf-4311-b53c-dd9413dcc133.mp4
