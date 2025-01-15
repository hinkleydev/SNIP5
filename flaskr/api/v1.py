from flask import Blueprint, jsonify, request
from cryptography.fernet import Fernet
import os

# All the data is publicly accessible why are we encrypting???
SECRET_KEY = Fernet.generate_key() # Wouldn't you like to know weatherboy?
encryptionHandler = Fernet(SECRET_KEY)
data = []

api = Blueprint('api', __name__)

# Create - Add snippet to the list
@api.post('/snippets')
def add():
    idList = [0]
    for each in data :
        idList.append(each["id"])
    idList.sort()
    nextId = idList[-1] + 1; # Get the next ID by organising the IDs and adding 1 to the biggest
    userInput = request.json # This rejects it if it isn't JSON
    if userInput.get("lang") == None :
        return jsonify({"error" : "lang not specified"})
    if userInput.get("data") == None :
        return jsonify({"error" : "data not specified"})
    # Check the object has the required fields and tell the user if not
    dataBytes = bytes(source=userInput["data"],encoding="utf-8")
    newObject = {
        "id" : nextId,
        "lang" : userInput["lang"],
        "data" : encryptionHandler.encrypt(dataBytes).decode(encoding="utf-8") # Encrypt for DB
    }
    data.append(newObject)
    # Make new object and add to array
    return jsonify({"id" : nextId, "lang" : userInput["lang"], "data" : userInput["data"]}), 201

# Root - Returns amount of snippets and languages in use
@api.get('/snippets')
def root():
    languages = []
    for each in data :
        languages.append(each["lang"])
    languages = set(languages) # Remove the duplicates
    languages = list(languages) # Remake list to add to JSON
    return jsonify({"snippets" : len(data), "languages" : languages})

# Specific - Returns all the details of a specific snippet
@api.route('/snippets/<int:id>')
def byID(id):
    for each in data :
        if id != each["id"] : continue # Pass if not what we're after
        rawData = each["data"]
        bytesData = bytes(source=rawData, encoding="utf-8")
        unencryptedData = encryptionHandler.decrypt(bytesData)
        unencryptedText = unencryptedData.decode(encoding="utf-8")
        return jsonify({ "id" : each["id"], "lang" : each["lang"], "data" : unencryptedText })
    return jsonify({"error" : "not found"}), 404 # Default if nothing is found