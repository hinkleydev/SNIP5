from flask import Blueprint, jsonify, request
from api.reader import data

api = Blueprint('api', __name__)

# Create - Add snippet to the list
@api.post('/snippets')
def add():
    idList = []
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
    newObject = {
        "id" : nextId,
        "lang" : userInput["lang"],
        "data" : userInput["data"]
    }
    data.append(newObject)
    # Make new object and add to array
    return jsonify(newObject), 201

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
        return jsonify(each)
    return jsonify({"error" : "not found"}), 404 # Default if nothing is found