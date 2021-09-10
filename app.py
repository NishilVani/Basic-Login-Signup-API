from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import ast

# Initializing App
app = Flask(__name__)
app.secret_key = 'Secret_Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///API.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

# Creating SQLite Database


class User_table(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    sids = db.Column(db.String, nullable=True)

# Basic Authentication
@auth.verify_password
def verify(username, password):
    user = User_table.query.filter_by(Username=username).first()
    if user:
        if check_password_hash(user.Password, password):
            return True
    return False

# Routes of API


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password1 = data['password1']
    password2 = data['password2']

    user = User_table.query.filter_by(Username=username).first()
    if user:
        return jsonify({'Signup': 'Username already exists,Try something unique.'})
    elif " " in username:
        return jsonify({'Signup': 'Username should not contain space.'})
    elif len(username) < 2:
        return jsonify({'Signup': 'Username is too short.'})
    elif len(password1) < 7:
        return jsonify({'Signup': 'Password is too short.'})
    elif password1 != password2:
        return jsonify({'Signup': 'Password doesn\'t match.'})
    else:
        new_user = User_table(
            Username=username, Password=generate_password_hash(password1, method='sha256'), sids='[]')
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'Signup': "Successfull"})


@app.route('/', methods=['POST'])
@auth.login_required
def Home():
    return jsonify('You are currently Loged In as ' + auth.current_user())


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    user = User_table.query.filter_by(Username=username).first()
    if user:
        if check_password_hash(user.Password, password):
            return jsonify({'Login': "Successfull"})
        else:
            return jsonify({'Login': 'Incorrect password, try again.'})
    else:
        return jsonify({'Login': 'User does not exist.'})


@app.route('/newpwd', methods=["POST"])
@auth.login_required
def newpwd():
    data = request.get_json()
    username = auth.current_user()
    user = User_table.query.filter_by(Username=username).first()
    password1 = data['password1']
    password2 = data['password2']
    if password1 != password2:
        return jsonify({'newpwd': 'Password doesn\'t match.'})
    elif len(password1) < 7:
        return jsonify({'newpwd': 'Password is too short.'})
    else:
        user.Password = generate_password_hash(password1, method='sha256')
        db.session.commit()

        return jsonify({'newpwd': 'Password changed Succesfully.'})

@socketio.on('addusername', namespace='/private')
def add_username(username):
    user = User_table.query.filter_by(Username=username).first()
    user_sids = ast.literal_eval(user.sids)
    user_sids.append(request.sid)
    user.sids = str(user_sids)
    db.session.commit()

@socketio.on('removeusername', namespace='/private')
def remove_username(username):
    print("yeah")
    user = User_table.query.filter_by(Username=username).first()
    user_sids = ast.literal_eval(user.sids)
    user_sids.remove(request.sid)
    user.sids = str(user_sids)
    db.session.commit()

@socketio.on('Recheck', namespace='/private')
def Recheck(username):
    user = User_table.query.filter_by(Username=username).first()
    user_sids = ast.literal_eval(user.sids)
    for i in range(0, len(user_sids)):
        if user_sids[i] != request.sid:
            emit('Reload', "Reload", room=user_sids[i])

if __name__ == '__main__':
    socketio.run(app)
