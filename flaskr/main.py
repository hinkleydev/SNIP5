from flask import Flask, request, abort, jsonify, redirect
from api.v1 import api
import bcrypt, jwt, os, requests
from cryptography.fernet import Fernet

users = []
SALT = bcrypt.gensalt()
JWT_TOKEN = os.environ["JWT_TOKEN"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

@api.before_request
def loggedIn() :
    try :
        jwt.decode(request.headers.get("Authorization", ""), JWT_TOKEN, algorithms=["HS256"])
        # This doesn't compare to the user, if they have a valid JWT, it can only have been issued by the server cause of the token
    except :
        abort(403, "Invalid authorization token recieved")

app = Flask(__name__)
app.register_blueprint(api, url_prefix = "/api/v1")

@app.post("/register")
def register() :
    data = request.json
    username = data["username"]
    password = data["password"]
    for user in users : # Stop if the user already exists
        if user["username"] == username :
            abort(400, "User already exists")
    passwordBytes = bytes(password, encoding="utf-8")
    hashBytes = bcrypt.hashpw(passwordBytes, SALT)
    hash = bytes.decode(hashBytes, encoding="utf-8")
    userObject = { "username" : username, "password" : hash }
    users.append(userObject)
    encoded = jwt.encode(userObject, JWT_TOKEN, algorithm="HS256")
    return jsonify({"status" : "success", "token" : encoded})

@app.post("/login")
def login() :
    data = request.json
    username = data["username"]
    password = data["password"]
    passwordBytes = bytes(password, encoding="utf-8")
    loggedInUser = None
    for user in users : 
        if user["username"] == username : # Found user
            hash = user["password"]
            hashBytes = bytes(hash, encoding="utf-8")
            if bcrypt.checkpw(passwordBytes, hashBytes): # Correct password
                loggedInUser = user
    if not loggedInUser :
        abort(401, "Incorrect login")
    encoded = jwt.encode(loggedInUser, JWT_TOKEN, algorithm="HS256")
    return jsonify({"status" : "success", "token" : encoded})

@app.get("/auth")
def redirect_auth():
    return redirect("https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID)

@app.get("/callback")
def authenticate():
    code = request.args["code"]
    r = requests.post("https://github.com/login/oauth/access_token", 
        json={"client_id" : CLIENT_ID, "client_secret" : CLIENT_SECRET, "code" : code},
        headers={"accept" : "application/json"})
    access_token = r.json()["access_token"]
    user = requests.get("https://api.github.com/user",
        headers={"Accept" : "application/json", "Content-Type" : "application/json", "Authorization" : "Bearer " + access_token})
    userValues = user.json()
    userObject = { "username" : userValues["login"], "password" : "GITHUB-USER" }
    users.append(userObject)
    encoded = jwt.encode(userObject, JWT_TOKEN, algorithm="HS256")
    return jsonify({"status" : "success", "token" : encoded})