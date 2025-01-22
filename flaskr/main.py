from flask import Flask, request, abort, jsonify
from api import v1
import bcrypt, jwt
from cryptography.fernet import Fernet

users = []
SALT = bcrypt.gensalt()
JWT_TOKEN = Fernet.generate_key()

app = Flask(__name__)

app.register_blueprint(v1.api, url_prefix = "/api/v1")

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

